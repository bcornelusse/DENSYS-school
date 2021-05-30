import json

from datetime import datetime, timedelta

from microgrid.control import *
from microgrid.history import Database
from microgrid.model import Grid
from microgrid.simulate import Simulator

# Simulation configuration
CASE = "application_data"
SIMULATE_FROM_DATE = datetime(2018, 1, 1, 0, 0, 0)
SIMULATE_TO_DATE = datetime(2018, 1, 15, 0, 0, 0)
STORE_ACTIONS = True

DATA_FILE = "examples/data/%s.json" % CASE
RESULTS_FILE = "results/%s_out.json" % CASE
import os

if not os.path.isdir("results"):
  os.mkdir("results")


# Load the microgrid instance
with open(DATA_FILE, 'rb') as jsonFile:
    data = json.load(jsonFile)
    microgrid = Grid(data)

# Build the forecaster
database = Database('examples/data/application_timeseries.csv', microgrid)

# Build the controller
controller = IdleController(microgrid, database)

# Build the simulator
simulator = Simulator(microgrid, controller, database)

# Run the simulation
grid_states = simulator.run(start_date=SIMULATE_FROM_DATE,
                            end_date=SIMULATE_TO_DATE)


# Export results
results = dict(dates=["%s" % d.date_time for d in grid_states],
               soc=[d.state_of_charge for d in grid_states],
               charge = [d.charge for d in grid_states],
               discharge = [d.discharge for d in grid_states],
               cum_total_cost=[d.cum_total_cost for d in grid_states],
               energy_cost=[d.energy_cost for d in grid_states],
               production=[d.production for d in grid_states],
               consumption=[d.consumption for d in grid_states],
               grid_export=[d.grid_export for d in grid_states],
               grid_import=[d.grid_import for d in grid_states],
               peak_cost=[d.peak_cost for d in grid_states])

print('Total cost = %s' % results["cum_total_cost"][-1])

if STORE_ACTIONS:
    results['actions'] = simulator.actions

with open(RESULTS_FILE, 'w') as jsonFile:
   json.dump(results, jsonFile)

from plot_results import Plotter

plotter = Plotter(results, 'results/%s' % CASE)
plotter.plot_results()
