import numpy as np

from datetime import datetime, timedelta
from sklearn.ensemble import ExtraTreesRegressor


class Forecaster:
    _ls_lower_bound_ = datetime(2014, 1, 1, 0, 0, 0)
    _dt_lower_bound_ = datetime(2015, 1, 1, 0, 0, 0)
    _dt_upper_bound_ = datetime(2015, 6, 30, 0, 0, 0)

    _ls_input_ = ['Year', 'Month', 'Day', 'Hour', 'Minutes', 'Seconds', 'IsoDayOfWeek',
                  'IsoWeekNumber']

    def __init__(self, database):
        """
        A Forecaster object allows to generate forecast of any of the uncertain quantities referenced in the database.

        :param database: A :class:`Database` object used for training the forecaster
        """
        self.database = database
        self._predicted_quantities_ = database._output_

    def forecast(self, column, dt_from, dt_to):
        """
        Forecast an uncertain quantity over a specified time range with a hourly resolution.
        Each time a forecast is asked, a new forecaster is trained using all previous values
        of the quantity until dt_from.

        :param column: Name of the series to forecast
        :param dt_from: A date_time object specifying the start of the prediction horizon
        :param dt_to: A date_time object specifying the end of the prediction horizon
        :return: The forecast as a numpy array. The length of the array is equal to the number of hours between dt_from and dt_to, rounded down
        """
        dt_from = dt_from.replace(minute=0, second=0, microsecond=0)
        dt_to = dt_to.replace(minute=0, second=0, microsecond=0)

        if column not in self._predicted_quantities_:
            raise ValueError('Cannot predict column %s' % column)
        if dt_from > dt_to:
            raise ValueError("From date time cannot be after to date time")
        if dt_from < Forecaster._dt_lower_bound_:
            raise ValueError('From date cannot be before %s' % Forecaster._dt_lower_bound_)
        if dt_from > Forecaster._dt_upper_bound_:
            raise ValueError('From date cannot be after %s' % Forecaster._dt_upper_bound_)
        if dt_to < Forecaster._dt_lower_bound_:
            raise ValueError('To date cannot be before %s' % Forecaster._dt_lower_bound_)
        if dt_to > Forecaster._dt_upper_bound_:
            raise ValueError('To date cannot be after %s' % Forecaster._dt_upper_bound_)

        shift_history_size = 48
        one_hour = timedelta(hours=1)

        dt_train_from = Forecaster._ls_lower_bound_
        dt_train_to = dt_from - one_hour

        df = self.database.data_frame
        df_x_ls = df[dt_train_from: dt_train_to].copy()
        df_y_ls = df_x_ls[column]

        # all previous values of the quantity
        shift_columns = []
        for tau in range(1, shift_history_size + 1):
            col_name = "%s(t-%d)" % (column, tau)
            df_x_ls[col_name] = df_y_ls.shift(tau)
            shift_columns.append(col_name)

        df_x_ls = df_x_ls.dropna(axis=0, how='any')

        X_train = df_x_ls.as_matrix(columns=Forecaster._ls_input_ + shift_columns)
        y_train = df_x_ls[column].as_matrix()

        clf = ExtraTreesRegressor(n_estimators=10)
        clf.fit(X_train, y_train)

        dt_test = dt_from

        date_diff = dt_to - dt_from
        days, seconds = date_diff.days, date_diff.seconds
        hours = days * 24 + seconds // 3600

        X_test_shifts = np.flipud(y_train[-shift_history_size:])

        h = 0
        y_pred = np.zeros((hours + 1))

        while dt_test <= dt_to:
            X_test_dt_infos = np.array([
                dt_test.year,
                dt_test.month,
                dt_test.day,
                dt_test.hour,
                dt_test.minute,
                dt_test.second,
                dt_test.isoweekday(),
                dt_test.isocalendar()[1]
            ])

            X_test_row = np.concatenate((X_test_dt_infos, X_test_shifts))
            X_test = np.tile(X_test_row, (1, 1))

            y_pred[h] = clf.predict(X_test)

            X_test_shifts = np.roll(X_test_shifts, 1, axis=0)
            X_test_shifts[0] = y_pred[h]

            h = h + 1
            dt_test = dt_test + one_hour

        return y_pred
