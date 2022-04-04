"""Scheduler manager"""

import pathlib
import random

from monitoring_project_api.service.logging import setup_logger
from . import scheduler
from .exceptions import LoggerRestoreError
from .tasks import TriggerIndividualCheck
from .tasks import individual_check
from ...models import Task


def scheduler_manager(
        processing_methods: list,
        *,
        logging_path: pathlib.Path = None,
) -> int:
    """
    Function that allows restoring scheduled tasks and configuring loggers
    :param processing_methods: A list of available processing methods
    :type processing_methods: list
    :param logging_path: The folder where the logging files will be stored
    :type logging_path: pathlib.Path
    :return: The number of restored tasks
    :rtype: int
    """
    # Check that logging path is not None
    if logging_path is None:
        raise LoggerRestoreError

    # Get tasks
    items = Task.get_all(active_only=True)

    # Iteration on items and creation of jobs
    for item in items:
        # Add job
        scheduler.add_job(
            func=individual_check,
            trigger=TriggerIndividualCheck(task=item),
            id=(f"individual_check_job_{item.id}_"
                f"{random.randint(0, 1000)}"),
            args=[item.id]
        )

        # Restore logger
        # Check folder
        logging_path = logging_path / f'{item.name} {item.id}'
        if not logging_path.is_dir():
            logging_path.mkdir(parents=True)

        for method in processing_methods:
            setup_logger(
                name=f'{item.id}_{method}',
                log_file=logging_path / f'{item.name} {item.id}' / f'{method}'
                                                                   f'.log'
            )

    return len(items)
