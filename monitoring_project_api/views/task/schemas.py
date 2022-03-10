"""Task API schemas"""
import datetime

import marshmallow as ma
from flask_smorest import abort
from marshmallow import ValidationError
from marshmallow_sqlalchemy import auto_field

from monitoring_project_api.extensions import AutoSchema
from monitoring_project_api.models import Task
from .data_schemas import DataModelSchema


class TaskModelSchema(AutoSchema):
    class Meta:
        table = Task.__table__

    @ma.validates("next_run_time")
    def validate_next_run_time(self, next_run_time):
        if next_run_time < datetime.datetime.now():
            raise ValidationError("Next run time must be greater than the "
                                  "actual time.")

    id = auto_field(dump_only=True)
    name = auto_field(validate=ma.validate.Length(1, 80))
    description = auto_field(
        validate=ma.validate.Length(max=500),
        required=False,
    )
    is_active = auto_field(
        required=True,
        dump_only=True,
    )
    task_frequency = auto_field(required=True)
    next_run_time = ma.fields.DateTime(
        required=True
    )
    last_run_time = ma.fields.DateTime(dump_only=True, required=False)
    try:
        target_data = ma.fields.Nested(DataModelSchema, required=True)
    except ValidationError as e:
        abort(422, message=e.args)
