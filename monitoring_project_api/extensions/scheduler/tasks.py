"""Scheduler tasks"""

import datetime as dt
from typing import NoReturn

from apscheduler.triggers.base import BaseTrigger

from monitoring_project_api.extensions.database import db
from monitoring_project_api.service import Detector
from monitoring_project_api.models import Task
from . import scheduler
from .exceptions import JobError


class TriggerAutoCheckJob(BaseTrigger):
    """AutoCheck trigger"""

    def get_next_fire_time(self, previous_fire_time, now):
        with scheduler.app.app_context():
            if previous_fire_time is None:
                return now + dt.timedelta(
                    seconds=scheduler.app.config['AUTO_CHECK_EXECUTE_AFTER']
                )
            return now + dt.timedelta(
                minutes=scheduler.app.config['AUTO_CHECK_INTERVAL']
            )


class TriggerIndividualCheck(BaseTrigger):
    """Individual check trigger"""

    def __init__(self, task):
        super().__init__()
        self.task = task

    def get_next_fire_time(self, previous_fire_time, now):
        if (
                previous_fire_time is None
                and self.task.remaining_time_to_execute_task()
        ):
            return self.task.next_run_time
        try:
            return previous_fire_time + self.task.task_frequency
        except TypeError:
            return now


@scheduler.task(
    trigger=TriggerAutoCheckJob(),
    alias='auto_check',
    id="auto_check_job",
    max_instances=1,
)
def auto_check():
    """Auto check job.
    Added when app starts.
    """
    items = db.session.query(Task).all()
    nb_processed_item = 0
    for item in items:
        if item.is_to_process():
            nb_processed_item = +1
            detector = Detector(task=item)
            detector.launch()

    with scheduler.app.app_context():
        scheduler.app.logger.debug(
            f"<Auto check> : number of processed items -> {nb_processed_item}")


def individual_check(task_id: int) -> NoReturn:
    """Individual check for every task.
    Added when a new task is posted.
    :param task_id: A task id.
    :type task_id: int
    """
    # Get task
    try:
        task = Task.get(task_id=task_id)
    except ValueError as e:
        raise JobError('Individual check error <Invalid task id>') from e

    if task.is_to_process():
        detector = Detector(task=task)
        detector.launch()
        return

    raise JobError('Individual check error <Next run time Problem>')
