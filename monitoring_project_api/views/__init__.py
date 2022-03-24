"""Resources initialization"""
from . import task
from . import task_properties

MODULES = [
    task,
    task_properties
]


def register_blueprints(api):
    """Initialize application with all modules"""
    for module in MODULES:
        module.register_blueprints(api)
