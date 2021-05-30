from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import numpy as np


plt.style.use('bmh')

#print(plt.style.available)
FONT_SIZE = 12

class Plotter:
    def __init__(self, results, case):
        """

        :param results: A json type dictionary containing results
        :param case: Name of the case, as a string
        """
        self.results = results
        self.case = case

        self.dates = [datetime.strptime(d, "%Y-%m-%d %H:%M:%S") for d in results["dates"]]

    def get_ticks(self, start, end):
        xstep = max(1, (end - start) / 24)
        dates = self.dates[start:end]
        xtick_labels = dates[::xstep]
        xticks = range(0, len(dates), xstep)
        return xticks, xtick_labels

    def plot_results(self, from_date=None, to_date=None):

        if from_date is None:
            from_date = self.dates[0]
        if to_date is None:
            to_date = self.dates[-1] - timedelta(hours=1)

        if from_date < self.dates[0]:
            raise ValueError('From date cannot be before %s' % self.dates[0])
        if to_date > self.dates[-1]:
            raise ValueError('To date cannot be after %s' % self.dates[-1])
        if to_date < from_date:
            raise ValueError('To date cannot be after from date')

        # Index of from_date in self.dates
        start = self.dates.index(from_date)
        end = self.dates.index(to_date)

        self.plot_batteries(start, end)
        self.plot_costs(start, end)
        self.plot_flows(start, end)

    def plot_batteries(self, start, end):

        xticks, xticks_labels = self.get_ticks(start, end)

        for b in range(len(self.results["soc"][0])):
            soc = [x[b] for x in self.results["soc"][start:end]]
            charge = [-x[b] for x in self.results["charge"][start:end]]
            discharge = [x[b] for x in self.results["discharge"][start:end]]

            fig = plt.figure(figsize=(16, 9))

            ax1 = plt.subplot(2, 1, 1)
            ax1.set_ylabel('kWh', fontsize=FONT_SIZE)
            ax1.plot(soc, 'k', label="State of charge")
            ax1.set_xticks(xticks)
            ax1.set_xticklabels(xticks_labels)
            ax1.legend(fontsize=FONT_SIZE)

            ax2 = plt.subplot(2, 1, 2, sharex=ax1)
            ax2.set_ylabel('kW', fontsize=FONT_SIZE)
            ax2.plot(discharge, label="Discharge", drawstyle='steps')
            ax2.plot(charge, label="Charge", drawstyle='steps')
            ax2.set_ylim([min(charge) * 1.1, max(discharge) * 1.1])
            ax2.legend(fontsize=FONT_SIZE)
            #ax2.axhline(y=0, color='k', lw=0.5)

            fig.autofmt_xdate()
            fig.savefig('%s_battery_%d.pdf' % (self.case, b))

    def plot_costs(self, start, end):

        xticks, xticks_labels = self.get_ticks(start, end)

        cum_total_cost = self.results["cum_total_cost"][start:end]
        energy_cost = self.results["energy_cost"][start:end]
        peak_cost = self.results["peak_cost"][start:end]

        fig = plt.figure(figsize=(16, 9))

        ax1 = plt.subplot(2, 1, 1)
        ax1.set_ylabel('EUR', fontsize=FONT_SIZE)
        ax1.plot(cum_total_cost, 'k', label="Cumulative total cost")
        ax1.set_xticks(xticks)
        ax1.set_xticklabels(xticks_labels)
        ax1.legend(fontsize=FONT_SIZE)

        ax2 = plt.subplot(2, 1, 2, sharex=ax1)
        ax2.set_ylabel('EUR', fontsize=FONT_SIZE)
        ax2.plot(energy_cost, label="Energy", drawstyle='steps')
        ax2.plot(peak_cost, label="Peak", drawstyle='steps')
        ax2.set_ylim([min(energy_cost)*1.1, max(max(energy_cost), max(peak_cost)) * 1.1])
        ax2.legend(fontsize=FONT_SIZE)
        #ax2.axhline(y=0, color='k', lw=0.5)

        fig.autofmt_xdate()
        fig.savefig('%s_costs.pdf' % self.case)

    def plot_flows(self, start, end):

        xticks, xticks_labels = self.get_ticks(start, end)

        exports = np.array(self.results["grid_export"][start:end])
        imports = np.array(self.results["grid_import"][start:end])
        net_export = exports - imports

        productions = self.results["production"][start:end]
        consumptions = [-x for x in self.results["consumption"]][start:end]

        fig = plt.figure(figsize=(16, 9))

        ax1 = plt.subplot(2, 1, 1)
        ax1.set_ylabel('kWh', fontsize=FONT_SIZE)
        ax1.plot(net_export, 'k', label="Net export to grid", drawstyle='steps')
        ax1.set_xticks(xticks)
        ax1.set_xticklabels(xticks_labels)
        ax1.legend(fontsize=FONT_SIZE)
        #ax1.axhline(y=0, color='k', lw=0.5)

        ax2 = plt.subplot(2, 1, 2, )
        ax2.set_ylabel('kW', fontsize=FONT_SIZE)
        ax2.plot(productions, label="Production", drawstyle='steps')
        ax2.plot(consumptions, label="Consumption", drawstyle='steps')
        ax2.set_ylim([min(consumptions) * 1.1, max(productions) * 1.1])
        ax2.set_xticks(xticks)
        ax2.set_xticklabels(xticks_labels)
        ax2.legend(fontsize=FONT_SIZE)
        #ax2.axhline(y=0, color='k', lw=0.5)

        fig.autofmt_xdate()
        fig.savefig('%s_flows.pdf' % self.case)


if __name__ == "__main__":
    import json

    CASE = "case1"

    with open("results/%s_out.json" % CASE, "rb") as json_results:
        results = json.load(json_results)

        plotter = Plotter(results, 'results/%s' % CASE)
        plotter.plot_results()
        #plotter.plot_results(from_date=datetime(2015, 6, 21, 0, 0, 0),
        #                     to_date=datetime(2015, 6, 25, 0, 0, 0))
