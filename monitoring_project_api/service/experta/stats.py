"""Statistic processing rules"""

from experta import *

from .facts import NotRequiredProperty
from .facts import ProcessingMethod


class StatisticProcessingRules:
    """
    Class which contains the rules related to the statistical processing
    methods (average_requests_per_time_interval...)
    """

    ###############
    # Accepted URLs
    ###############
    @Rule(
        AND(
            ProcessingMethod(method='ACCEPTED_URLS_METHOD'),
            NotRequiredProperty(property_name='accepted_urls')
        )
    )
    def accepted_urls_method_update_workflow(self):
        """
        The rule allows to update the workflow by adding the
        `ACCEPTED_URLS_METHOD` and its parameters.
        """
        # Update detector `workflow` dictionary
        self.detector.workflow = ('ACCEPTED_URLS_METHOD', {
            'accepted_urls': self.not_required_properties['accepted_urls']
        })

    @Rule(
        AND(
            ProcessingMethod(method='ACCEPTED_URLS_METHOD'),
            NOT(NotRequiredProperty(property_name='accepted_urls')),
        )
    )
    def define_accepted_urls_parameter(self) -> None:
        """
        The rule allows to define the parameter `accepted_urls` of the
        `ACCEPTED_URLS_METHOD` processing method (If it is not specified by the
        user).
        """
        self.not_required_properties['accepted_urls'] = ['/']
        self.declare(NotRequiredProperty(property_name='accepted_urls'))

    ##################
    # Black IP address
    ##################
    @Rule(
        AND(
            ProcessingMethod(method='BLACK_IP_ADDRESS_METHOD'),
            NotRequiredProperty(property_name='black_ip_address')
        )
    )
    def black_ip_address_method_update_workflow(self):
        """
        The rule allows to update the workflow by adding the
        `BLACK_IP_ADDRESS_METHOD` and its parameters.
        """
        # Update detector `workflow` dictionary
        self.detector.workflow = ('BLACK_IP_ADDRESS_METHOD', {
            'black_ip_address': self.not_required_properties[
                'black_ip_address']
        })

    @Rule(
        AND(
            ProcessingMethod(method='BLACK_IP_ADDRESS_METHOD'),
            NOT(NotRequiredProperty(property_name='black_ip_address')),
        )
    )
    def define_black_ip_address_parameter(self) -> None:
        """
        The rule allows to define the parameter `black_ip_address` of the
        `BLACK_IP_ADDRESS_METHOD` processing method (If it is not specified by
        the user).
        """
        self.not_required_properties['black_ip_address'] = []
        self.declare(NotRequiredProperty(property_name='black_ip_address'))
