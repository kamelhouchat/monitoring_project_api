"""Resources initialization"""
from . import task

MODULES = [
    task
]


def register_blueprints(api):
    """Initialize application with all modules"""
    for module in MODULES:
        module.register_blueprints(api)
