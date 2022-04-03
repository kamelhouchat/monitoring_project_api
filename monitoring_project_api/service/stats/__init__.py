"""Stats processing method package"""

from .accepted_urls import AcceptedURLsDetector
from .black_ip_address import BlackIpAddressDetector

STATS_PROCESSING_METHODS = {
    "ACCEPTED_URLS_METHOD": AcceptedURLsDetector,
    "BLACK_IP_ADDRESS_METHOD": BlackIpAddressDetector,
    # "average_requests_per_time_interval": 1,
    # "average_requests_per_client_per_time_interval": 1,
    # "black_ip_address": 1,
    # "is_http_requests_accepted": 1,
}
