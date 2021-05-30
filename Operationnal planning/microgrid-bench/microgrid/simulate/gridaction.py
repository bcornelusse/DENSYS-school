class GridAction():
    def __init__(self, grid_import, grid_export, production,
                 consumption, state_of_charge, charge,
                 discharge, peak, peak_increase):
        """
        Action taken by the controller. Actually, the action is only a subset of the parameters
        and other members represent auxiliary information that may be used for reporting purposes.

        Each action is defined per device, then per period of the optimization horizon.
        Each member is defined as a list or as nested lists.


        :param grid_import: Auxiliary variable.
        :param grid_export: Auxiliary variable.
        :param production: Auxiliary variable.
        :param consumption: Auxiliary variable.
        :param state_of_charge: Auxiliary variable.
        :param charge: Action to charge storage devices.
        :param discharge: Action to discharge storage devices.
        :param peak: Auxiliary variable.
        :param peak_increase: Auxiliary variable.
        """

        self.grid_import = grid_import
        self.grid_export = grid_export
        self.production = production
        self.consumption = consumption
        self.state_of_charge = state_of_charge
        self.charge = charge
        self.discharge = discharge
        self.peak = peak
        self.peak_increase = peak_increase

    def to_json(self):
        return self.__dict__
