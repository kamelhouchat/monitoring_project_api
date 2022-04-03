"""Black ip address detector"""

import logging
from typing import get_type_hints

import pandas as pd

from .exceptions import BlackIPAddressException
from ..method_base import DetectionMethod


class BlackIpAddressDetector(DetectionMethod):
    """
    Class which allows detecting black ip adresses.
    """

    # noinspection PyUnusedLocal
    def __init__(self,
                 *,
                 dataframe: pd.DataFrame,
                 black_ip_address: list,
                 logger: logging.Logger,
                 **kwargs: dict) -> None:
        """
        Class initializer.
        :param dataframe: The original dataframe.
        :type dataframe: pd.DataFrame
        :param black_ip_address: A list that contains the blacklisted ip
        addresses
        :type black_ip_address: list
        :param logger: The detection method logger
        :type logger: logging.Logger
        :param kwargs: Other potential parameters
        :type dict
        """
        self.dataframe = dataframe

        # Parse parameter
        try:
            black_ip_address = get_type_hints(self.__init__)[
                'black_ip_address'](black_ip_address)
        except (TypeError, ValueError) as e:
            raise BlackIPAddressException('Invalid parameter -> '
                                          '`black_ip_address`') from e

        # Check that `black_ip_address` is not empty
        if not len(black_ip_address):
            raise BlackIPAddressException(
                '`black_ip_address` parameter must contains at least one '
                'element !')

        self.black_ip_address = black_ip_address

        # Init the logger
        self.logger = logger

    def launch(self) -> None:
        """
        Method used to start the processing
        """
        # Filter the dataframe according to the blacklisted IPs
        anomalies = self.dataframe[
            self.dataframe['remote'].isin(self.black_ip_address)]

        # Log anomalies
        if len(anomalies):
            self.logger.warning(
                '\t' + anomalies.to_string().replace('\n', '\n\t'))
