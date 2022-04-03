"""Experta Facts"""

import schema
from experta import Fact
from experta import Field

from monitoring_project_api.models.init_db_values import PROCESSING_METHODS
from monitoring_project_api.models.init_db_values import \
    TASK_PROPERTY_DEFAULT_VALUES


class NotRequiredProperty(Fact):
    """
    Fact which will represent all possible values for the not required `task
    property` fields.
    example:
    - black_ip_address
    - average_requests_per_time_interval
    - is_http_requests_accepted
    - ...
    """
    property_name = Field(
        schema.Or(*[
            task_property['name'] for task_property in
            TASK_PROPERTY_DEFAULT_VALUES
        ]),
        mandatory=True
    )


class ProcessingMethod(Fact):
    """
    Fact that represents the processing method (must be on of supported method)
    """
    method = Field(
        schema.Or(*[*PROCESSING_METHODS]),
        mandatory=True
    )
