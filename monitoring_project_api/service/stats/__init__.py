"""Stats processing method package"""

from .accepted_urls import AcceptedURLsDetector
from .average_requests_per_time_interval import \
    AverageRequestsPerTimeIntervalDetector
from .black_ip_address import BlackIpAddressDetector
from .is_http_requests_accepted import IsHTTPRequestsAcceptedDetector

STATS_PROCESSING_METHODS = {
    "ACCEPTED_URLS_METHOD": AcceptedURLsDetector,
    "BLACK_IP_ADDRESS_METHOD": BlackIpAddressDetector,
    "IS_HTTP_REQUESTS_ACCEPTED_METHOD": IsHTTPRequestsAcceptedDetector,
    "AVERAGE_REQUESTS_PER_TIME_INTERVAL_METHOD": AverageRequestsPerTimeIntervalDetector,
    # "average_requests_per_client_per_time_interval": 1,
}
