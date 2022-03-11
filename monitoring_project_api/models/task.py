"""Task model"""

import ast
import time
from enum import Enum

import marshmallow as ma
import sqlalchemy as sqla
import sqlalchemy.event as sqla_event

from monitoring_project_api.extensions.database import Base
from monitoring_project_api.extensions.database import db
from .data import Data

try:
    from .init_db_values import TASK_PROPERTY_DEFAULT_VALUES  # noqa
except ImportError:
    import sys

    init_db_values = sys.modules[__package__ + '.init_db_values']


class Task(Base):
    __tablename__ = "tasks"

    _target_data = None

    id = sqla.Column(
        sqla.Integer(),
        primary_key=True,
    )
    name = sqla.Column(
        sqla.String(80),
        nullable=False,
    )
    description = sqla.Column(
        sqla.Text(length=500),
        nullable=True,
    )
    is_active = sqla.Column(
        sqla.Boolean(),
        nullable=False,
        default=True,
    )
    task_frequency = sqla.Column(
        sqla.Interval(native=False),
        nullable=False
    )
    next_run_time = sqla.Column(
        sqla.DateTime(),
        nullable=False
    )
    last_run_time = sqla.Column(
        sqla.DateTime(),
        nullable=True
    )
    target_data_id = sqla.Column(
        sqla.Integer(),
        sqla.ForeignKey('data.id'),
        nullable=False
    )

    @property
    def target_data(self) -> Data:
        """
        Property that allows to retrieve the target data of the current task.
        :rtype: Data
        :return: The target data of the current task.
        """
        if self._target_data is None:
            self._target_data = Data.get(self.target_data_id)
        return self._target_data

    def __repr__(self):
        return (
            f"<{self.__class__.__name__}("
            f"id={self.id}"
            f", name={self.name}"
            f", description={self.description}"
            f", task_frequency={self.task_frequency}"
            f", next_run_time={self.next_run_time}"
            f", last_run_time={self.last_run_time}"
            f", is_active={self.is_active}"
            ")>")

    def remaining_time_to_execute_task(self) -> float:
        """
        Method that return the remaining time before the next run.
        :return: The remaining time before the next execution (unix timestamp).
        :rtype: float
        """
        return max(self.next_run_time.timestamp() - time.time(), 0)

    def is_to_process(self) -> bool:
        """
        Method which returns a boolean to indicate whether the task must be
        executed when the method is called.
        :return: A boolean which indicates if the task must be executed.
        :rtype: bool
        """
        return not bool(self.remaining_time_to_execute_task())

    @classmethod
    def get_all(cls, *, active_only: bool = True) -> list:
        """
        Class method that returns all the current tasks.
        :param active_only: if False, the deleted tasks will be included.
        :type active_only: bool
        :return: A list which contains all the tasks.
        :rtype: list
        """
        stmt = db.session.query(cls)
        if active_only:
            return stmt.filter_by(is_active=True).all()
        return stmt.all()

    @classmethod
    def get(cls, task_id: int):
        """
        Class method that return a task associated with the given ID.
        :param task_id: The task id.
        :type task_id int
        :return: A task associated with the given ID.
        """
        result = db.session.get(cls, task_id)
        if result is None:
            raise ValueError(f'{task_id} is not a valid id.')
        return result


class TaskPropertyTypeEnum(Enum):
    Int = ma.fields.Integer
    Float = ma.fields.Float
    String = ma.fields.String
    Boolean = ma.fields.Boolean
    List = ma.fields.List

    def to_python(self, value_in):
        if value_in is not None:
            if self is self.__class__.Int:
                return int(value_in)
            elif self is self.__class__.Float:
                return float(value_in)
            elif self is self.__class__.String:
                return str(value_in)
            elif self is self.__class__.Boolean:
                if isinstance(value_in, str):
                    value_in = 1 if value_in.lower() == "true" else 0
                return bool(value_in)
            elif self is self.__class__.List:
                # ast protect from code injection
                try:
                    parsed_list = ast.literal_eval(value_in)
                except (SyntaxError, ValueError):
                    return value_in if isinstance(value_in, list) else None
                if isinstance(parsed_list, list):
                    return parsed_list
        return None


class TaskProperty(Base):
    __tablename__ = "task_properties"

    id = sqla.Column(
        sqla.Integer(),
        primary_key=True
    )
    name = sqla.Column(
        sqla.String(20),
        nullable=False
    )
    description = sqla.Column(
        sqla.Text(length=500),
        nullable=True,
    )
    type = sqla.Column(
        sqla.Enum(TaskPropertyTypeEnum),
        nullable=True
    )

    def get_ma_type(self) -> ma.fields:
        """
        Method used to return the marshmallow field corresponding to the
        current value.
        :rtype: marshmallow.fields
        :return: The marshmallow field corresponding to the current value.
        """
        return self.type.value

    @classmethod
    def get_all(cls) -> list:
        """
        Class method which allows to retrieve all the properties.
        :return: The list of properties.
        :rtype: list
        """
        return db.session.query(cls).all()

    @classmethod
    def get_by_names(cls, names_list: list) -> list:
        """
        Class method that allows to select properties that have specific names
        (passed as a parameter).
        :rtype: list
        :param names_list: The list of names (to filter the search).
        :return: The result of the query.
        """
        return db.session.query(
            cls
        ).filter(
            cls.name.in_(names_list)
        ).all()


class TaskByProperty(Base):
    __tablename__ = "task_by_properties"

    __table_args__ = (
        sqla.UniqueConstraint(
            'task_id',
            'task_property_id'
        ),
        sqla.PrimaryKeyConstraint(
            'task_id',
            'task_property_id'
        )
    )

    task_id = sqla.Column(
        sqla.Integer(),
        sqla.ForeignKey('tasks.id'),
        nullable=False
    )
    task_property_id = sqla.Column(
        sqla.Integer(),
        sqla.ForeignKey('task_properties.id'),
        nullable=False
    )
    value = sqla.Column(
        sqla.String(100),
        nullable=False
    )


# noinspection PyUnusedLocal
@sqla_event.listens_for(TaskProperty.__table__, 'after_create')
def _insert_initial_task_property(target, connection, **kwargs):
    # add default task property
    for value in init_db_values.TASK_PROPERTY_DEFAULT_VALUES:
        connection.execute(
            target.insert(),
            value
        )
