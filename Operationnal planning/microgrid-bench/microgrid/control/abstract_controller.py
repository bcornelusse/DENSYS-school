from abc import ABCMeta, abstractmethod


class AbstractController(object):
    __metaclass__ = ABCMeta

    def __init__(self, grid):
        self.grid = grid

    @abstractmethod
    def compute_actions(self, start_date, end_date, grid_state, horizon, debug=False):

        """
        :param start_date: Start period for which actions is requested
        :param end_date: End period for which actions is requested
        :param grid_state: State of the grid at start_period
        :param horizon: optimization horizon
        :param debug: flag to (de)active debug information
        :return: grid actions to be applied to the microgrid, as a GridAction object
        """
        pass
