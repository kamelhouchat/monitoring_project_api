"""Initial database values"""

from .task import TaskPropertyTypeEnum

#######
# TASKS
#######

TASK_PROPERTIES_ID_LIST = [
    "BLACK_IP_ADDRESS_ID",
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
    }
]

TASK_PROPERTY_VALIDATOR = {
    # Three types of validator are possible: OneOf, Range and Required
    # - OneOf keys must have a list as value
    # - Range keys must have a dict with this four parameters as values:
    #     - min
    #     - max
    #     - min_inclusive (Boolean)
    #     - max_inclusive (Boolean)
    # - Required keys must have a boolean as value

    TASK_ID_BY_PROPERTIES['BLACK_IP_ADDRESS_ID']: {
        "Required": False
    }
}
