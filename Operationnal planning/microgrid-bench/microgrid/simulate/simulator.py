from datetime import timedelta
from .gridstate import GridState


def datetime_range(start, end, delta):
    current = start
    if not isinstance(delta, timedelta):
        delta = timedelta(**delta)
    while current < end:
        yield current
        current += delta


TOL_IS_ZERO = 1e-4


class Simulator:
    def __init__(self, grid, controller, database):
        """
        :param grid: A description of the grid as a Grid object
        :param controller: tool that decides, based on a forecast, a grid state and a model, which decisions to apply to the system now, until the next reoptimization
        :param database: (true) evolution of the exogeneous quantities over the simulation period
        """
        self.grid = grid
        self.controller = controller
        self.database = database
        self.actions = {}

    def run(self, start_date, end_date, decision_horizon=1, optim_horizon=24):
        """
        Run the simulation.

        :param start_date: start period of the simulation
        :param end_date: end period of the simulation
        :param decision_horizon: resolution of the simulation, in hours
        :param optim_horizon: parameter passed to the controller in case the latter computes decisions over an optimization horizon longer than 1 period.
        :return:
        """

        grid_states = [GridState(self.grid, start_date)]  # Initialize the grid with a default state

        for dt in datetime_range(start_date, end_date, {'hours': decision_horizon}):

            print("Simulating from %s for the next %d hour(s)" % (dt, decision_horizon))
            dt_from = dt
            dt_to = dt + timedelta(hours=decision_horizon)

            # Get the control actions
            actions = self.controller.compute_actions(dt_from, dt_to, grid_states[-1],
                                                      optim_horizon)

            self.actions[dt_from.strftime('%y/%m/%d_%H')] = actions.to_json()

            # Apply the control actions
            n_storages = len(self.grid.storages)

            for p in range(decision_horizon):
                p_dt = dt + timedelta(hours=p)
                next_grid_state = GridState(self.grid, dt + timedelta(hours=p))

                actual_charge = [0.0] * n_storages
                actual_discharge = [0.0] * n_storages
                for b in range(n_storages):
                    storage = self.grid.storages[b]

                    # Take care of potential simultaneous charge and discharge.
                    actual_charge[b] = actions.charge[b][p]
                    actual_discharge[b] = actions.discharge[b][p]
                    if actual_charge[b] > TOL_IS_ZERO and actual_discharge[b] > TOL_IS_ZERO:
                        net = actual_charge[b] - actual_discharge[b]
                        if net > TOL_IS_ZERO:
                            actual_charge[b] = net
                        elif net < -TOL_IS_ZERO:
                            actual_discharge[b] = -net

                    # Update battery SOC based on its detailed model
                    if actual_charge[b] > TOL_IS_ZERO:
                        planned_evolution = grid_states[-1].state_of_charge[b] \
                                            + actual_charge[b] * storage.charge_efficiency
                        next_grid_state.state_of_charge[b] = min(storage.capacity,
                                                                 planned_evolution)
                    elif actual_discharge[b] > TOL_IS_ZERO:
                        planned_evolution = grid_states[-1].state_of_charge[b] \
                                            - actual_discharge[b] / storage.discharge_efficiency
                        next_grid_state.state_of_charge[b] = max(0.0, planned_evolution)
                    else:
                        next_grid_state.state_of_charge[b] = grid_states[-1].state_of_charge[b]

                next_grid_state.charge = actual_charge[:]
                next_grid_state.discharge = actual_discharge[:]

                # Aggregate realizations of exogenous consumption and generation variables
                realized_non_flexible_production = 0.0
                for g in self.grid.generators:
                    realized_non_flexible_production += self.database.get_columns(g.name, p_dt)

                # realized_non_flexible_consumption = 0.0
                # for l in self.grid.loads:
                #     realized_non_flexible_consumption += self.database.get_columns(l.name, p_dt)

                # the consumption is given by the controller since part of the consumption is scheduled
                realized_consumption = actions.consumption[p]

                # we check at the end of each day whether the total consumption of the day given by the controller
                # matches the consumption of the day in the time series.

                if dt.hour == 23:
                    day_controller_realized_consumption = realized_consumption
                    for t_prev in range(23):
                        day_controller_realized_consumption += grid_states[-1-t_prev].realized_consumption

                    day_data_realized_consumption = 0
                    for t_prev in range(24):
                        dt_prev = p_dt - timedelta(hours=t_prev)
                        for l in self.grid.loads:
                            day_data_realized_consumption += self.database.get_columns(l.name, dt_prev)

                    day_realized_consumption_difference = day_controller_realized_consumption - day_data_realized_consumption

                    assert -TOL_IS_ZERO < day_realized_consumption_difference < TOL_IS_ZERO, \
                        "The daily consumption does not correspond to the timeseries data"


                # Deduce actual production and consumption
                actual_production = realized_non_flexible_production \
                                    + sum(actual_discharge[b] for b in range(n_storages))
                actual_consumption = realized_consumption \
                                     + sum(actual_charge[b] for b in range(n_storages))
                next_grid_state.production = actual_production
                next_grid_state.consumption = actual_consumption
                next_grid_state.realized_consumption = realized_consumption

                actual_import = actual_export = 0
                net_import = actual_consumption - actual_production
                current_peak = 0.0
                if net_import > TOL_IS_ZERO:
                    actual_import = net_import * self.grid.period_duration
                    current_peak = actual_import
                elif net_import < -TOL_IS_ZERO:
                    actual_export = -net_import * self.grid.period_duration

                next_grid_state.grid_import = actual_import
                next_grid_state.grid_export = actual_export

                actual_purchase_price = self.database.get_columns("purchase_price", p_dt)
                actual_sale_price = self.database.get_columns("sale_price", p_dt)
                # actual_energy_price = [self.database.get_columns("Price", p_dt)]
                # actual_purchase_price = self.grid.purchase_price(actual_energy_price)[0]
                # actual_sale_price = self.grid.sale_price(actual_energy_price)[0]
                energy_cost = actual_import * actual_purchase_price \
                              - actual_export * actual_sale_price
                next_grid_state.energy_cost = energy_cost

                # Compute the peak and update the state
                past_peaks = grid_states[-1].past_peaks[:]

                month_of_current_period = p_dt.month
                month_of_previous_period = (p_dt - timedelta(hours=1)).month

                peak_cost_increment = 0.0
                max_past_peaks = 0.0
                if month_of_previous_period != month_of_current_period:  # It is the first period of the month
                    past_peaks.pop(0)
                    max_past_peaks = max(past_peaks)
                    peak_cost_increment = max_past_peaks * self.grid.peak_price
                    past_peaks.append(current_peak)
                else:
                    max_past_peaks = max(past_peaks)
                    past_peaks[-1] = max(past_peaks[-1], current_peak)

                if current_peak > max_past_peaks:
                    peak_cost_increment += (current_peak - max_past_peaks) * self.grid.peak_price

                next_grid_state.past_peaks = past_peaks
                next_grid_state.peak_cost = peak_cost_increment

                # Total_cost
                next_grid_state.cum_total_cost = grid_states[-1].cum_total_cost + energy_cost \
                                                 + peak_cost_increment

                # Update the state evolution list
                grid_states.append(next_grid_state)

        return grid_states
