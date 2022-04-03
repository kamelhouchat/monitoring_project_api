"""Experta decision-making helpers package"""

from ipaddress import AddressValueError
from ipaddress import IPv4Address
from pathlib import Path
from typing import Iterator

from .exceptions import ExpertaHelpersException


def get_default_ip_list(ip_file_path: Path = None) -> Iterator[str]:
    """
    Function that returns a list of black IPs read from a file
    :param ip_file_path: A path to the file that contains ip addresses
    :type ip_file_path: Path
    :return A generator of ip addresses list
    :rtype Iterator[str]
    """
    if ip_file_path is None:
        # Get file path
        ip_file_path = Path(__file__).parent.parent.parent.parent / \
                       'assets/ip_list.txt'

    # Read the file and generate list
    with open(ip_file_path, mode='r') as file:
        # Read lines
        for line in file:
            # Strip line (remove `\n`)
            line = line.strip()

            # Validate IP
            try:
                IPv4Address(line)
            except AddressValueError as e:
                raise ExpertaHelpersException(f'Invalid IP address -> {line}') \
                    from e

            yield line
