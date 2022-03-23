"""Extra validators"""

from ipaddress import AddressValueError
from ipaddress import IPv4Address

from flask_smorest import abort

__all__ = [
    'black_list_validation',
    'average_requests_per_time_interval_validation'
]


def black_list_validation(data):
    """
    Function used to validate each IP address present in the `black_list` list.
    :param data: Data entered by the user.
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


def average_requests_per_time_interval_validation(data):
    """
    Function which validate the field `average_requests_per_time_interval`.
    :param data: Data entered by the user.
    :type data: dict
    :return: NoReturn
    """
    # Check that `average_requests_per_time_interval` is not None
    if 'average_requests_per_time_interval' not in data['properties']:
        return

    # Retrieve the property dictionary
    time_interval_per_request = data['properties'][
        'average_requests_per_time_interval']

    # Ordered dictionary key iterator
    ordered_dict_key_iterator = iter(
        sorted(time_interval_per_request.keys(), key=lambda x: int(x))
    )

    # Get the first value key
    value = time_interval_per_request[next(ordered_dict_key_iterator)]

    # Iterate over the others values and validate
    for key in ordered_dict_key_iterator:
        if (next_value := time_interval_per_request[key]) < int(value):
            abort(422, message="Invalid field "
                               "`average_requests_per_time_interval`")
        value = next_value
