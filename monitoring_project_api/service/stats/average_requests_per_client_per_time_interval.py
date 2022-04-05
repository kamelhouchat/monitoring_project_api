"""Average requests per client per time interval detector"""

import logging
from typing import get_type_hints

import pandas as pd

from .exceptions import AverageRequestsPerClientPerTimeIntervalException
from ..method_base import DetectionMethod


class AverageRequestsPerClientPerTimeIntervalDetector(DetectionMethod):
    """
    Class which allows detecting if a number of abused request per client is
    made.
    """

    # noinspection PyUnusedLocal
    def __init__(self,
                 *,
                 dataframe: pd.DataFrame,
                 average_requests_per_client_per_time_interval: dict,
                 logger: logging.Logger,
                 **kwargs: dict) -> None:
        """
        Class initializer.
        :param dataframe: The original dataframe.
        :type dataframe: pd.DataFrame
        :param average_requests_per_client_per_time_interval: dictionary that
        associates the time intervals with the maximum number of requests
        :type average_requests_per_client_per_time_interval: dict
        :param logger: The detection method logger
        :type logger: logging.Logger
        :param kwargs: Other potential parameters
        :type dict
        """
        self.dataframe = dataframe

        # Parse parameter
        try:
            average_requests_per_client_per_time_interval = get_type_hints(
                self.__init__)[
                'average_requests_per_client_per_time_interval'](
                average_requests_per_client_per_time_interval)
        except (TypeError, ValueError) as e:
            raise AverageRequestsPerClientPerTimeIntervalException(
                'Invalid parameter -> '
                '`average_requests_per_client_per_time_interval`'
            ) from e

        # Check that dictionary is not empty
        if not len(average_requests_per_client_per_time_interval):
            raise AverageRequestsPerClientPerTimeIntervalException(
                'The dictionary `average_requests_per_client_per_time_interv'
                'al` must have at least one element'
            )

        self.average_requests_per_client_per_time_interval = \
            average_requests_per_client_per_time_interval

        # Init the logger
        self.logger = logger

    def launch(self) -> None:
        """
        Method used to start the processing
        """
        # Set timestamp as dataframe index
        dataframe_copy = self.dataframe.set_index(self.dataframe['timestamp'])

        # Process dataframe
        for index in dataframe_copy.index:
            for timedelta, auth_nb_request in \
                    self.average_requests_per_client_per_time_interval.items():
                # Calculate next time according to the time interval
                step = index + pd.Timedelta(f'{timedelta}s')

                # Select data
                selected_data = dataframe_copy.loc[index:step]

                # Count values and detect anomalies
                counted_values = selected_data['remote'].value_counts()
                anomalies = counted_values.where(
                    counted_values >= auth_nb_request
                ).dropna()

                # Log anomalies
                for idx in anomalies.index:
                    self.logger.warning(f'Number of allowed requests exceeded'
                                        f' {idx} - {index} to {step} '
                                        f'({timedelta} seconds) -> '
                                        f'{anomalies[idx]} requests (accepted:'
                                        f' {auth_nb_request})')
