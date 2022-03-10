"""Task model"""

import time

import sqlalchemy as sqla
import sqlalchemy.orm as sqla_orm

from monitoring_project_api.extensions.database import Base
from monitoring_project_api.extensions.database import db


class Task(Base):
    __tablename__ = "tasks"

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

    target_data = sqla_orm.relationship(
        "Data",
        primaryjoin="Data.id == Task.target_data_id",
    )

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
