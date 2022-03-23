"""Task API schemas"""

import datetime
import gc

import marshmallow as ma
from flask_smorest import abort
from marshmallow import ValidationError
from marshmallow_sqlalchemy import auto_field

from monitoring_project_api.extensions import AutoSchema
from monitoring_project_api.extensions import Schema
from monitoring_project_api.models import TASK_PROPERTY_VALIDATOR
from monitoring_project_api.models import Task
from monitoring_project_api.models import TaskProperty
from . import extra_validators
from .data_schemas import DataModelSchema


class MetaCreateSchema(ma.schema.SchemaMeta):
    def __new__(mcs, classname, bases, namespace, **kwargs):
        for task_property in namespace['_meta_kwargs']:

            # validators = []
            # required = True
            kwargs = {
                "required": True,
                "validators": []
            }
            # Get the corresponding validators
            if task_property.id in \
                    TASK_PROPERTY_VALIDATOR:
                for validator_type, parameters in \
                        TASK_PROPERTY_VALIDATOR[
                            task_property.id].items():
                    if validator_type == 'OneOf':
                        kwargs["validators"].append(ma.validate.OneOf(parameters))
                    elif validator_type == 'range':
                        kwargs["validators"].append(ma.validate.Range(**parameters))
                    elif validator_type in ['required', 'keys', 'values']:
                        kwargs[validator_type] = parameters

            # Get the corresponding marshmallow field
            ma_type = task_property.get_ma_type()
            if ma_type == ma.fields.List:
                marshmallow_field = ma_type(ma.fields.Str, **kwargs)
            else:
                marshmallow_field = ma_type(**kwargs)

            # Adding the field to the schema
            namespace[task_property.name] = marshmallow_field

        # Inherit from the schema class of marshmallow (flask_smorest)
        bases = (Schema,)
        return super().__new__(mcs, classname, bases, namespace)


# noinspection PyUnresolvedReferences
class TaskModelSchema(AutoSchema):
    class Meta:
        table = Task.__table__

    # noinspection PyUnusedLocal
    @ma.post_dump
    def post_dump_preprocessing(self, data, *args, **kwargs):
        # The post-processing allows to change the types of fields (int,
        # float, string) instead of returning strings all time

        # No need to look for all task
        if 'properties' not in data:
            return data

        # Get properties
        properties = TaskProperty.get_by_names(
            data['properties'].keys())

        typed_properties = {}
        for (property_name, property_value), db_property in \
                zip(data['properties'].items(), properties):
            if db_property is None:
                abort(404)
            typed_properties[
                property_name] = db_property.type.to_python(property_value)
        data['properties'] = typed_properties
        return data

    # noinspection PyUnusedLocal
    @ma.validates_schema
    def validate_properties(self, data, *args, **kwargs):
        # Do not validate if there are no properties.
        if 'properties' not in data:
            return data

        # Get properties
        properties = TaskProperty.get_by_names(
            data['properties'].keys())

        class PropertiesSchema(metaclass=MetaCreateSchema):
            _meta_kwargs = properties

        # Validation of properties fields
        properties_schema = PropertiesSchema()
        try:
            properties_schema.load(data['properties'])
        except ValidationError as e:
            abort(422, message=e.args)

        # Deleting the dynamically generated schema and forcing the garbage
        # collector
        del PropertiesSchema
        gc.collect()

        # Run logical validators
        for validator in extra_validators.__all__:
            extra_validators.__dict__[validator](data)

        return data

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
    properties = ma.fields.Dict(
        required=False,
        metadata={
            'description': "Task properties as dictionary.",
            'example': {
                'black_ip_address': ['192.168.0.0']
            }
        }
    )
    try:
        target_data = ma.fields.Nested(DataModelSchema, required=True)
    except ValidationError as e:
        abort(422, message=e.args)
