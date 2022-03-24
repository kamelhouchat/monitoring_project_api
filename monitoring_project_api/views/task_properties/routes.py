"""Task property resources"""

from flask.views import MethodView
from flask_smorest import abort

from monitoring_project_api.extensions import Blueprint
from monitoring_project_api.extensions.database import db
from monitoring_project_api.models import TaskProperty
from .schemas import TaskPropertyQueryArgsSchema
from .schemas import TaskPropertySchema

bp = Blueprint(
    "Task property resources", __name__, url_prefix="/task_properties",
    description="Operation on task_properties",
)


@bp.route('/')
class TaskPropertyViews(MethodView):

    @bp.arguments(TaskPropertyQueryArgsSchema, location='query')
    @bp.response(200, TaskPropertySchema(many=True))
    def get(self, args):
        """List of task_properties"""
        return db.session.query(TaskProperty).filter_by(**args)


@bp.route('/<int:item_id>')
class TaskPropertyByIdViews(MethodView):

    @bp.response(200, TaskPropertySchema)
    def get(self, item_id):
        """Get task_property by id"""
        item = db.session.get(TaskProperty, item_id)
        if item is None:
            abort(404)
        return item
