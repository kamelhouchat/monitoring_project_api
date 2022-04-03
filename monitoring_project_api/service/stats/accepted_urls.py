"""Accepted urls detector"""

import logging
from typing import get_type_hints

import pandas as pd

from .exceptions import AcceptedURLsException
from ..method_base import DetectionMethod


class AcceptedURLsDetector(DetectionMethod):
    """
    Class which allows detecting if an unaccepted url is queried.
    """

    # noinspection PyUnusedLocal
    def __init__(self,
                 *,
                 dataframe: pd.DataFrame,
                 accepted_urls: list,
                 logger: logging.Logger,
                 **kwargs: dict) -> None:
        """
        Class initializer.
        :param dataframe: The original dataframe.
        :type dataframe: pd.DataFrame
        :param accepted_urls: A list that contains the accepted URLs
        :type accepted_urls: list
        :param logger: The detection method logger
        :type logger: logging.Logger
        :param kwargs: Other potential parameters
        :type dict
        """
        self.dataframe = dataframe

        # Parse parameter
        try:
            accepted_urls = get_type_hints(self.__init__)[
                'accepted_urls'](accepted_urls)
        except (TypeError, ValueError) as e:
            raise AcceptedURLsException('Invalid parameter -> '
                                        '`accepted_urls`') from e

        # Check that `accepted_urls` is not empty
        if not len(accepted_urls):
            raise AcceptedURLsException(
                '`accepted_urls` parameter must contains at least one '
                'element !')

        self.accepted_urls = accepted_urls

        # Init the logger
        self.logger = logger

    def launch(self, *, add_root_path: bool = True) -> None:
        """
        Method used to start the processing
        :param add_root_path: If True, accept the root path
        :type add_root_path: bool
        """
        # Drop query args from URLs
        self.dataframe['not_accepted_urls_path'] = self.dataframe['path'].map(
            lambda x: x.split('?')[0], na_action='ignore'
        )

        # Add root path
        if add_root_path:
            self.accepted_urls.append('/')

        # Filter the dataframe according to the accepted URLs
        anomalies = self.dataframe[
            ~self.dataframe['not_accepted_urls_path'].isin(self.accepted_urls)]

        # Log anomalies
        if len(anomalies):
            self.logger.warning(
                '\t' + anomalies.to_string().replace('\n', '\n\t'))

        # Drop added columns
        self.dataframe.drop('not_accepted_urls_path', axis=1, inplace=True)
