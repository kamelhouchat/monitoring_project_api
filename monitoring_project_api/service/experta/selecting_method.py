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
            NotRequiredProperty(property_name='black_ip_address')
        )
    )
    def select_black_ip_address_method(self):
        """
        The rule allows to select the method `BLACK_IP_ADDRESS_METHOD` if the
        parameter `black_ip_address` is filed by the user.
        """
        # Declare the fact
        self.declare(ProcessingMethod(method="BLACK_IP_ADDRESS_METHOD"))
