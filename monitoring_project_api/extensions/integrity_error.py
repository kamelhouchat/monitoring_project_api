"""Integrity error management

Catch integrity errors in resources and return appropriate error code.
"""
import contextlib

import sqlalchemy as sqla
from flask_smorest import abort


class catch_integrity_error(contextlib.ContextDecorator):
    """Context manager catching integrity errors

    Can be used as context manager or decorator.
    """
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        # noinspection PyUnresolvedReferences
        if exc_type and issubclass(exc_type, sqla.exc.IntegrityError):
            abort(409, message=f"IntegrityError: {exc_value.orig}")
        return False
