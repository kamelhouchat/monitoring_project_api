"""Selecting method rules"""

from experta import *

from .facts import NotRequiredProperty
from .facts import ProcessingMethod


class SelectingMethodRules:
    """
    Class which contains the rules related to the selection of the processing
    methods
    """

    ###############
    # Accepted URLs
    ###############
    @Rule(
        AND(
            NOT(ProcessingMethod(method='ACCEPTED_URLS_METHOD')),
            NotRequiredProperty(property_name='accepted_urls')
        )
    )
    def select_accepted_urls_method(self):
        """
        The rule allows to select the method `ACCEPTED_URLS_METHOD` if the
        parameter `accepted_urls` is filed by the user.
        """
        # Declare the fact
        self.declare(ProcessingMethod(method="ACCEPTED_URLS_METHOD"))

    ##################
    # Black IP address
    ##################
    @Rule(
        AND(
            NOT(ProcessingMethod(method='BLACK_IP_ADDRESS_METHOD')),
        )
    )
    def select_black_ip_address_method(self):
        """
        The rule allows to select the method `BLACK_IP_ADDRESS_METHOD`
        """
        # Declare the fact
        self.declare(ProcessingMethod(method="BLACK_IP_ADDRESS_METHOD"))

    ###########################
    # Is http requests accepted
    ###########################
    @Rule(
        AND(
            NOT(ProcessingMethod(method='IS_HTTP_REQUESTS_ACCEPTED_METHOD')),
            NotRequiredProperty(property_name='is_http_requests_accepted')
        )
    )
    def select_black_ip_address_method(self):
        """
        The rule allows to select the method `IS_HTTP_REQUESTS_ACCEPTED_METHOD`
        if the parameter `is_http_requests_accepted` is filed by the user.
        """
        # Declare the fact
        self.declare(ProcessingMethod(
            method="IS_HTTP_REQUESTS_ACCEPTED_METHOD"))

    ####################################
    # Average requests per time interval
    ####################################
    @Rule(
        AND(
            NOT(ProcessingMethod(
                method='AVERAGE_REQUESTS_PER_TIME_INTERVAL_METHOD')),
            NotRequiredProperty(
                property_name='average_requests_per_time_interval')
        )
    )
    def select_average_requests_per_time_interval_method(self):
        """
        The rule allows to select the method
        `AVERAGE_REQUESTS_PER_TIME_INTERVAL_METHOD` if the parameter
        `average_requests_per_time_interval` is filed by the user.
        """
        # Declare the fact
        self.declare(ProcessingMethod(
            method="AVERAGE_REQUESTS_PER_TIME_INTERVAL_METHOD"))
