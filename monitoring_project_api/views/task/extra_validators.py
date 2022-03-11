"""Extra validators"""

from ipaddress import AddressValueError
from ipaddress import IPv4Address

from flask_smorest import abort

__all__ = [
    'black_list_validation',
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
