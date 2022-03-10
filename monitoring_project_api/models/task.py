"""Task model"""

import time

import sqlalchemy as sqla

from monitoring_project_api.extensions.database import Base
from monitoring_project_api.extensions.database import db
from monitoring_project_api.models import Data


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
