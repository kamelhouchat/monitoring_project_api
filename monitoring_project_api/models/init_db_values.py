"""Initial database values"""

import marshmallow as ma

from .task import TaskPropertyTypeEnum

#######
# TASKS
#######

TASK_PROPERTIES_ID_LIST = [
    "BLACK_IP_ADDRESS_ID",
    "AVERAGE_REQUESTS_PER_TIME_INTERVAL_ID",
    "IS_HTTP_REQUESTS_ACCEPTED_ID"
]

TASK_ID_BY_PROPERTIES = {
    property_name: property_id
    for property_id, property_name in enumerate(TASK_PROPERTIES_ID_LIST)
}

TASK_PROPERTY_DEFAULT_VALUES = [
    {
        "id": TASK_ID_BY_PROPERTIES['BLACK_IP_ADDRESS_ID'],
        "name": 'black_ip_address',
        "description": "A list of black IP addresses",
        "type": TaskPropertyTypeEnum.List.name,
    },
    {
        "id": TASK_ID_BY_PROPERTIES['AVERAGE_REQUESTS_PER_TIME_INTERVAL_ID'],
        "name": 'average_requests_per_time_interval',
        "description": "The average number of requests per time interval",
        "type": TaskPropertyTypeEnum.Dict.name,
    },
    {
        "id": TASK_ID_BY_PROPERTIES['IS_HTTP_REQUESTS_ACCEPTED_ID'],
        "name": 'is_http_requests_accepted',
        "description": "A boolean that indicate if the http requests are "
                       "considered as an anomalous",
        "type": TaskPropertyTypeEnum.Boolean.name,
    }
]

TASK_PROPERTY_VALIDATOR = {
    # Four types of validator are possible: OneOf, Range and Required
    # - OneOf keys must have a list as value
    # - range keys must have a dict with this four parameters as values:
    #     - min
    #     - max
    #     - min_inclusive (Boolean)
    #     - max_inclusive (Boolean)
    # - required keys must have a boolean as value
    # - keys and values must have a marshmallow.fields as value (its only used
    #   with properties of type Dict)

    TASK_ID_BY_PROPERTIES['BLACK_IP_ADDRESS_ID']: {
        "required": False
    },
    TASK_ID_BY_PROPERTIES['AVERAGE_REQUESTS_PER_TIME_INTERVAL_ID']: {
        "required": False,
        "keys": ma.fields.Int(),
        "values": ma.fields.Int()
    },
    TASK_ID_BY_PROPERTIES['IS_HTTP_REQUESTS_ACCEPTED_ID']: {
        "required": False
    }
}
