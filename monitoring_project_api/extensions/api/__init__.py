"""Api extension initialization"""
import http
from copy import deepcopy
from functools import wraps

import flask_smorest
import marshmallow as ma
import marshmallow.orderedset
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from .. import integrity_error


class Api(flask_smorest.Api):
    """Api Override"""

    def init_app(self, app, *, spec_kwargs=None):
        """API class"""
        super().init_app(app, spec_kwargs=spec_kwargs)


class Blueprint(flask_smorest.Blueprint):
    """Blueprint class"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @staticmethod
    def catch_integrity_error(func=None):
        """Catch DB integrity errors"""

        # noinspection PyShadowingNames
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                with integrity_error.catch_integrity_error():
                    return func(*args, **kwargs)

            # Store doc in wrapper function
            # The deepcopy avoids modifying the wrapped function doc
            wrapper._apidoc = deepcopy(getattr(wrapper, '_apidoc', {}))
            wrapper._apidoc.setdefault(
                'response', {}
            ).setdefault('responses', {})[409] = http.HTTPStatus(409).name

            return wrapper

        if func is None:
            return decorator
        return decorator(func)


class Schema(ma.Schema):
    """Schema class"""

    # Ensures the fields are ordered
    set_class = ma.orderedset.OrderedSet

    def update(self, obj, data):
        """Update object nullifying missing data"""
        loadable_fields = [
            k for k, v in self.fields.items() if not v.dump_only
        ]
        for name in loadable_fields:
            setattr(obj, name, data.get(name))


class AutoSchema(SQLAlchemyAutoSchema, Schema):
    """AutoSchema class"""


class SQLCursorPage(flask_smorest.Page):
    """SQL Cursor Pager class"""
