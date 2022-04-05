"""Average requests per time interval detector"""

import logging
from typing import get_type_hints

import pandas as pd

from .exceptions import AverageRequestsPerTimeIntervalException
from ..method_base import DetectionMethod


class AverageRequestsPerTimeIntervalDetector(DetectionMethod):
    """
    Class which allows detecting if a number of abused request is made.
    """

    # noinspection PyUnusedLocal
    def __init__(self,
                 *,
                 dataframe: pd.DataFrame,
                 average_requests_per_time_interval: dict,
                 logger: logging.Logger,
                 **kwargs: dict) -> None:
        """
        Class initializer.
        :param dataframe: The original dataframe.
        :type dataframe: pd.DataFrame
        :param average_requests_per_time_interval: dictionary that associates
        the time intervals with the maximum number of requests
        :type average_requests_per_time_interval: dict
        :param logger: The detection method logger
        :type logger: logging.Logger
        :param kwargs: Other potential parameters
        :type dict
        """
        self.dataframe = dataframe

        # Parse parameter
        try:
            average_requests_per_time_interval = get_type_hints(self.__init__)[
                'average_requests_per_time_interval'](
                average_requests_per_time_interval)
        except (TypeError, ValueError) as e:
            raise AverageRequestsPerTimeIntervalException(
                'Invalid parameter -> '
                '`average_requests_per_'
                'time_interval`'
            ) from e

        # Check that dictionary is not empty
        if not len(average_requests_per_time_interval):
            raise AverageRequestsPerTimeIntervalException(
                'The dictionary `average_requests_per_time_interval` must'
                'have at least one element'
            )

        self.average_requests_per_time_interval = \
            average_requests_per_time_interval

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
            for timedelta, auth_nb_request \
                    in self.average_requests_per_time_interval.items():
                step = index + pd.Timedelta(f'{timedelta}s')
                if (
                        nb_request := dataframe_copy.loc[index:step].shape[0]
                ) > auth_nb_request:
                    self.logger.warning(f'Number of allowed requests exceeded'
                                        f' {index} to {step} ({timedelta} '
                                        f'seconds) -> {nb_request} requests'
                                        f' (accepted: {auth_nb_request})')
