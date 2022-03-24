"""Extra validators"""

from ipaddress import AddressValueError
from ipaddress import IPv4Address
from typing import NoReturn

from flask_smorest import abort

__all__ = [
    'black_list_validation',
    'average_requests_per_time_interval_validation'
]


def black_list_validation(data: dict) -> None:
    """
    Function used to validate each IP address present in the `black_list` list
    :param data: Data entered by the user
    :type data: dict
    :return: NoReturn
    """
    # Check that `black_ip_address` is not None
    if 'black_ip_address' not in data['properties']:
        return

    # Iterate over IPs and use a builtin module `ipaddress` to validate it.
    for ip in data['properties']['black_ip_address']:
        try:
            IPv4Address(ip)
        except AddressValueError as e:
            abort(422, message=e.args)


def average_requests_per_time_interval_validation(data: dict) -> NoReturn:
    """
    Function which validate the field `average_requests_per_time_interval`
    :param data: Data entered by the user
    :type data: dict
    :return: NoReturn
    """
    # Initialize a list containing the names of the fields which will be
    # validated
    properties_name = [
        'average_requests_per_time_interval',
        'average_requests_per_client_per_time_interval'
    ]

    for property_name in properties_name:
        # Check that `property_name` is in task properties
        if property_name in data['properties']:
            # Retrieve the property dictionary
            time_interval_per_request = data['properties'][
                property_name]

            _validate_time_interval(
                data_with_interval=time_interval_per_request,
                property_name=property_name
            )


def _validate_time_interval(
        *, data_with_interval: dict, property_name: str) -> NoReturn:
    """
    Function that checks that time intervals are logical. Below, an example of
    an invalid entry:
    "average_requests_per_time_interval": {
        "254": 123,
        "255": 124,
        "180": 50,
        "170": 40,
        "152": 60
    }
    If we can accept 60 requests per 150 seconds then: we must accept at least
    150 requests per 180 seconds
    :param data_with_interval: Dictionary that contains the property that will
    be validated
    :type data_with_interval: dict
    :param property_name: The name of the property (Used to customize the abort
    message.).
    :type property_name: str
    """
    # Ordered dictionary key iterator
    ordered_dict_key_iterator = iter(
        sorted(data_with_interval.keys(), key=lambda x: int(x))
    )

    # Get the first value key
    value = data_with_interval[next(ordered_dict_key_iterator)]

    # Iterate over the others values and validate
    for key in ordered_dict_key_iterator:
        if (next_value := data_with_interval[key]) < int(value):
            abort(422, message="Invalid field "
                               f"`{property_name}`")
        value = next_value
