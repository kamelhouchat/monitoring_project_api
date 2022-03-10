"""Data model"""

import sqlalchemy as sqla

from monitoring_project_api.extensions.database import Base
from monitoring_project_api.extensions.database import db


class Data(Base):
    __tablename__ = "data"

    id = sqla.Column(
        sqla.Integer(),
        primary_key=True
    )
    path = sqla.Column(
        sqla.String(150),
        nullable=False
    )

    def __repr__(self):
        return (
            f"<{self.__class__.__name__}("
            f"id={self.id}"
            f", path={self.path}"
            ")>"
        )

    @classmethod
    def get(cls, data_id: int):
        """
        Class method that return a data associated with the given ID.
        :param data_id: The task id.
        :type data_id int
        :return: A data associated with the given ID.
        """
        result = db.session.get(cls, data_id)
        if result is None:
            raise ValueError(f'{data_id} is not a valid id.')
        return result
