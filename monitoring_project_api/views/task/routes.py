"""Task resources"""
import random

from flask.views import MethodView

from monitoring_project_api.extensions import Blueprint
from monitoring_project_api.extensions.database import db
from monitoring_project_api.extensions.scheduler import scheduler
from monitoring_project_api.models import Data
from monitoring_project_api.models import Task
from .schemas import TaskModelSchema
from ...extensions.scheduler.tasks import TriggerIndividualCheck
from ...extensions.scheduler.tasks import individual_check

bp = Blueprint(
    "Task resources", __name__, url_prefix="/tasks",
    description="Operation on tasks",
)


def add_data(data: dict) -> int:
    """
    Function that allows to add a data to the `Data` table.
    :param data: A dictionary which contains all the fields of a data of type
    `Data`.
    :return: The ID of the newly added item.
    :rtype: int
    """
    data_item = Data(**data)
    db.session.add(data_item)
    db.session.commit()
    return data_item.id


@bp.route("/")
class TaskViews(MethodView):

    @bp.etag
    @bp.response(200, TaskModelSchema(many=True))
    def get(self):
        """List tasks

        Route which allows to retrieve all the `current` tasks.
        """
        return db.session.query(Task)

    @bp.etag
    @bp.arguments(TaskModelSchema)
    @bp.response(201, TaskModelSchema)
    @bp.catch_integrity_error
    def post(self, new_item):
        """Add a new task

        Route which allows to add a new task.
        """
        # Extract data
        target_data = new_item.pop('target_data')

        # Add target data
        target_data_id = add_data(target_data)

        # Add a task
        new_item['target_data_id'] = target_data_id
        item = Task(**new_item)
        db.session.add(item)
        db.session.commit()

        # Create a task to process the data.
        scheduler.add_job(
            func=individual_check,
            trigger=TriggerIndividualCheck(task=item),
            id=f"individual_check_job_{item.id}_{random.randint(0, 1000)}",
            args=[item.id]
        )

        return item
