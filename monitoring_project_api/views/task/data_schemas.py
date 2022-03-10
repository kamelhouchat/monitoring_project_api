"""Data schemas"""

from pathlib import Path

import marshmallow as ma
from marshmallow import ValidationError
from marshmallow_sqlalchemy import auto_field

from monitoring_project_api.extensions import AutoSchema
from monitoring_project_api.models import Data


class DataModelSchema(AutoSchema):
    class Meta:
        table = Data.__table__

    id = auto_field(dump_only=True)
    path = ma.fields.URL(
        relative=False,
        require_tld=False,
        validate=ma.validate.Length(10, 150)
    )
