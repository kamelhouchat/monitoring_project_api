"""Is http requests accepted detector"""

import logging
from typing import get_type_hints

import pandas as pd

from .exceptions import IsHTTPRequestsAcceptedException
from ..method_base import DetectionMethod


class IsHTTPRequestsAcceptedDetector(DetectionMethod):
    """
    Class which allows detecting http requests.
    """

    # noinspection PyUnusedLocal
    def __init__(self,
                 *,
                 dataframe: pd.DataFrame,
                 is_http_requests_accepted: bool,
                 logger: logging.Logger,
                 **kwargs: dict) -> None:
        """
        Class initializer.
        :param dataframe: The original dataframe.
        :type dataframe: pd.DataFrame
        :param is_http_requests_accepted: A boolean that indicates if http
        requests are accepted
        :type is_http_requests_accepted: bool
        :param logger: The detection method logger
        :type logger: logging.Logger
        :param kwargs: Other potential parameters
        :type dict
        """
        self.dataframe = dataframe

        # Parse parameter
        try:
            is_http_requests_accepted = get_type_hints(self.__init__)[
                'is_http_requests_accepted'](is_http_requests_accepted)
        except (TypeError, ValueError) as e:
            raise IsHTTPRequestsAcceptedException('Invalid parameter -> '
                                                  '`is_http_requests_accepted`'
                                                  ) from e

        self.is_http_requests_accepted = is_http_requests_accepted

        # Init the logger
        self.logger = logger

    def launch(self) -> None:
        """
        Method used to start the processing
        """
        pass
        # TODO: make processing
