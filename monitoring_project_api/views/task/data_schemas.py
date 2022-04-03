"""Data schemas"""

import marshmallow as ma
from marshmallow_sqlalchemy import auto_field

from monitoring_project_api.extensions import AutoSchema
from monitoring_project_api.models import Data


# noinspection PyUnresolvedReferences
class DataModelSchema(AutoSchema):
    class Meta:
        table = Data.__table__

    @ma.validates_schema
    def validate_properties(self, data, *args, **kwargs):
        if 'auth_user_name' in data or 'auth_password' in data:
            if 'auth_user_name' not in data:
                abort(422, message="Missing `auth_user_name`")
            if 'auth_password' not in data:
                abort(422, message="Missing `auth_password`")

    id = auto_field(dump_only=True)
    os_host = auto_field(required=True, validate=ma.validate.Length(5, 150))
    os_port = auto_field(
        validate=ma.validate.Range(min=1024, max=49151, max_inclusive=True)
    )
    is_using_ssl = auto_field(required=True, default=True)
    auth_user_name = auto_field(
        required=False,
        validate=ma.validate.Length(1, 20)
    )
    auth_password = auto_field(
        required=False,
        validate=ma.validate.Length(1, 50)
    )
    indice = auto_field(required=True, validate=ma.validate.Length(1, 30))
