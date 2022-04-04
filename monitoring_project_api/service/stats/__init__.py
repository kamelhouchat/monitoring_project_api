"""Stats processing method package"""

from .accepted_urls import AcceptedURLsDetector
from .black_ip_address import BlackIpAddressDetector
from .is_http_requests_accepted import IsHTTPRequestsAcceptedDetector

STATS_PROCESSING_METHODS = {
    "ACCEPTED_URLS_METHOD": AcceptedURLsDetector,
    "BLACK_IP_ADDRESS_METHOD": BlackIpAddressDetector,
    "IS_HTTP_REQUESTS_ACCEPTED_METHOD": IsHTTPRequestsAcceptedDetector,
    # "average_requests_per_time_interval": 1,
    # "average_requests_per_client_per_time_interval": 1,
    # "black_ip_address": 1,
}
