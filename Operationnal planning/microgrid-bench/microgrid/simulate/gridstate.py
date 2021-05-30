class GridState:
    def __init__(self, grid, date_time):
        """
        Representation of the state of the system in the simulator. The state includes the state
        of charge of storage devices plus information regarding past operation of the system.

        :param grid: A Grid object
        :param date_time: The time at which the system in this state
        """
        self.grid = grid
        n_storages = len(self.grid.storages)
        self.date_time = date_time

        # List of state of charge for all storage devices, initialized at half of their capacity
        self.state_of_charge = [s.capacity/2.0 for s in self.grid.storages]
        self.past_peaks = [0.0] * 12 # List of peak power import over the last 12 monthes
        self.cum_total_cost = 0.0 # EUR Cumulative total energy cost to date
        self.energy_cost = 0.0 # EUR
        self.peak_cost = 0.0 # EUR

        # Auxiliary info
        self.grid_import = 0.0
        self.grid_export = 0.0
        self.production = 0.0
        self.consumption = 0.0
        self.realized_consumption = 0.0
        self.charge = [0.0] * n_storages
        self.discharge = [0.0] * n_storages
