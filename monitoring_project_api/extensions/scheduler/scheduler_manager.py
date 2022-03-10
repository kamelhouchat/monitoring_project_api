"""Scheduler manager"""

import random

from . import scheduler
from .tasks import TriggerIndividualCheck
from .tasks import individual_check
from ...models import Task


def scheduler_manager():
    # Get tasks
    items = Task.get_all(active_only=True)

    # Iteration on items and creation of jobs
    for item in items:
        scheduler.add_job(
            func=individual_check,
            trigger=TriggerIndividualCheck(task=item),
            id=(f"individual_check_job_{item.id}_"
                f"{random.randint(0, 1000)}"),
            args=[item.id]
        )

    return len(items)
