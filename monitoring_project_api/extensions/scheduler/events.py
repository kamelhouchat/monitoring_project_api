"""Scheduler events manager"""

from apscheduler.events import EVENT_JOB_ADDED
from apscheduler.events import EVENT_JOB_EXECUTED
from apscheduler.events import EVENT_JOB_REMOVED

from monitoring_project_api.extensions.database import db
from . import scheduler
from monitoring_project_api.models import Task


def job_added(event):
    with scheduler.app.app_context():
        if event.job_id != "auto_check_job":
            scheduler.app.logger.debug(f'<{event.job_id}> task was added !')


def job_removed(event):
    """Job removed event"""
    with scheduler.app.app_context():
        scheduler.app.logger.debug(f'<{event.job_id}> task was removed !')


def job_executed(event):
    """Job executed event"""
    with scheduler.app.app_context():
        if 'individual_check_job_' in event.job_id:
            split_id = event.job_id.split('_')
            task = db.session.get(Task, split_id[-2])
            scheduler.app.logger.debug(
                f"A task <{task.name}> has just been executed."
            )
            return
        scheduler.app.logger.debug(
            f"Auto check was done, next check in "
            f"{scheduler.app.config['AUTO_CHECK_INTERVAL']} minutes"
        )


scheduler.add_listener(job_added, EVENT_JOB_ADDED)
scheduler.add_listener(job_executed, EVENT_JOB_EXECUTED)
scheduler.add_listener(job_removed, EVENT_JOB_REMOVED)
