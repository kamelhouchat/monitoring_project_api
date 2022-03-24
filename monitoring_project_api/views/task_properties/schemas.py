"""Task Property API schemas"""

import marshmallow as ma
from marshmallow_sqlalchemy import auto_field

from monitoring_project_api.extensions import AutoSchema
from monitoring_project_api.extensions import Schema
from monitoring_project_api.models import TaskProperty
from monitoring_project_api.models.task import TaskPropertyTypeEnum


class TaskPropertySchema(AutoSchema):
    class Meta:
        table = TaskProperty.__table__

    id = auto_field(dump_only=True)
    name = auto_field(
        required=True,
        validate=ma.validate.Length(1, 80)
    )
    description = auto_field(
        validate=ma.validate.Length(max=500),
        required=False,
    )
    type = ma.fields.String(
        validate=ma.validate.OneOf([x.name for x in TaskPropertyTypeEnum]),
        required=True,
    )

    # noinspection PyUnusedLocal
    @ma.pre_dump
    def pre_dump_role(self, data, **kwargs):
        data.type = data.type.name
        return data


class TaskPropertyQueryArgsSchema(Schema):
    name = ma.fields.String(validate=ma.validate.Length(1, 80))
