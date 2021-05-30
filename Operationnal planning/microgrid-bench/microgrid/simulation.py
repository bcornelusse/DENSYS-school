import os
import json
from datetime import datetime

from copy import deepcopy

from microgrid.history import Database
from microgrid.model import Grid
from microgrid.simulate import Simulator


class SimulationConfiguration():
    def __init__(self, params=None):
        if params is not None:
            data = deepcopy(params)
        else:
            data = {}

        self.null_threshold = 1.e-6
        self.DECISION_HORIZON = data.pop("DECISION_HORIZON", 1)
        self.OPTIMIZATION_HORIZON = data.pop("OPTIMIZATION_HORIZON", 12)
        self.STORE_CONTROLLER_ACTIONS = data.pop("STORE_CONTROLLER_ACTIONS", True)

    @property
    def DECISION_HORIZON(self):
        """ Horizon over which decisions are applied """
        return self._DECISION_HORIZON

    @DECISION_HORIZON.setter
    def DECISION_HORIZON(self, value):
        assert isinstance(value, int) or isinstance(value, float)
        assert float(value) > self.null_threshold
        self._DECISION_HORIZON = int(value)

    @property
    def OPTIMIZATION_HORIZON(self):
        """ Horizon over which decisions are computed """
        return self._OPTIMIZATION_HORIZON

    @OPTIMIZATION_HORIZON.setter
    def OPTIMIZATION_HORIZON(self, value):
        assert isinstance(value, int) or isinstance(value, float)
        assert float(value) > self.null_threshold
        self._OPTIMIZATION_HORIZON = int(value)

    @property
    def STORE_CONTROLLER_ACTIONS(self):
        """ Shall controller actions be stored in the results file """
        return self._STORE_CONTROLLER_ACTIONS

    @STORE_CONTROLLER_ACTIONS.setter
    def STORE_CONTROLLER_ACTIONS(self, value):
        assert isinstance(value, int) or isinstance(value, float)
        self._STORE_CONTROLLER_ACTIONS = bool(value)


class Simulation():
    def __init__(self, case, start_date, end_date, config=SimulationConfiguration()):
        """

        :param case: Case name, as a string
        :param start_date: Start of simulation, datetime
        :param end_date: End of simulation, datetime
        :param config: Simulation configuration options, instance of SimulationConfiguration
        """

        self.case = case
        self.start_date = start_date
        self.end_date = end_date
        self.config = config

        # Definition of path to results and input
        self.MICROGRID_CONFIG_FILE = "data/%s.json" % self.case
        self.MICROGRID_DATA_FILE = 'data/%s_dataset.csv' % self.case
        self.RESULTS_FOLDER = "results_%s_%s" % (
            self.case, datetime.now().strftime('%Y-%m-%d_%H:%M:%S'))
        self.RESULTS_FILE = "%s/%s_out.json" % (self.RESULTS_FOLDER, self.case)

        # Load the microgrid instance
        with open(self.MICROGRID_CONFIG_FILE, 'rb') as jsonFile:
            data = json.load(jsonFile)
            self.microgrid = Grid(data)

        # Build the forecaster
        self.database = Database(self.MICROGRID_DATA_FILE, self.microgrid)

    def run(self, controller, store_results=True, generate_plots=True):
        """
        :param controller: Instance of a controller derived from AbstractController
        :param store_results: Boolean to trigger dump of results in results folder
        :param generate_plots: Boolean to trigger plot of results in results folder
        :return:
        """

        # Build the simulator
        self.simulator = Simulator(self.microgrid, controller, self.database)

        grid_states = self.simulator.run(start_date=self.start_date,
                                         end_date=self.end_date,
                                         decision_horizon=self.config.DECISION_HORIZON,
                                         optim_horizon=self.config.OPTIMIZATION_HORIZON)

        results = dict(dates=["%s" % d.date_time for d in grid_states],
                       soc=[d.state_of_charge for d in grid_states],
                       charge=[d.charge for d in grid_states],
                       discharge=[d.discharge for d in grid_states],
                       cum_total_cost=[d.cum_total_cost for d in grid_states],
                       energy_cost=[d.energy_cost for d in grid_states],
                       peak_cost=[d.peak_cost for d in grid_states],
                       production=[d.production for d in grid_states],
                       consumption=[d.consumption for d in grid_states],
                       grid_import=[d.grid_import for d in grid_states],
                       grid_export=[d.grid_export for d in grid_states])

        if self.config.STORE_CONTROLLER_ACTIONS:
            results['actions'] = self.simulator.actions

        if store_results or generate_plots:
            if not os.path.isdir(self.RESULTS_FOLDER):
                os.mkdir(self.RESULTS_FOLDER)

        if store_results:
            with open(self.RESULTS_FILE, 'w') as jsonFile:
                json.dump(results, jsonFile)

        if generate_plots:
            from microgrid.plot import Plotter

            plotter = Plotter(results, '%s/%s' % (self.RESULTS_FOLDER, self.case))
            plotter.plot_results()

        return results
