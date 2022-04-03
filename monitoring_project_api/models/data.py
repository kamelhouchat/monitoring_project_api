"""Data model"""

from typing import Union

import sqlalchemy as sqla

from monitoring_project_api.extensions.database import Base
from monitoring_project_api.extensions.database import db


class Data(Base):
    __tablename__ = "data"

    id = sqla.Column(
        sqla.Integer(),
        primary_key=True
    )
    os_host = sqla.Column(
        sqla.String(150),
        nullable=False
    )
    os_port = sqla.Column(
        sqla.Integer(),
        nullable=False
    )
    is_using_ssl = sqla.Column(
        sqla.Boolean(),
        nullable=False,
        default=True
    )
    auth_user_name = sqla.Column(
        sqla.String(20),
        nullable=True
    )
    auth_password = sqla.Column(
        sqla.String(50),
        nullable=True
    )
    indice = sqla.Column(
        sqla.String(30),
        nullable=False
    )

    def __repr__(self):
        return (
            f"<{self.__class__.__name__}("
            f"id={self.id}"
            f", os_host={self.os_host}"
            f", os_port={self.os_port}"
            f", is_using_ssl={self.is_using_ssl}"
            f", indice={self.indice}"
            ")>"
        )

    @classmethod
    def get(cls, data_id: int, as_dict: bool = False) -> Union['Data', dict]:
        """
        Class method that return a data associated with the given ID
        :param data_id: The task id
        :type data_id: int
        :param as_dict: If `True`, return a dict else, return `Data` instance
        :type as_dict: bool
        :return: A data associated with the given ID
        :rtype: Union[Data, dict]
        """
        result = db.session.get(cls, data_id)
        if result is None:
            raise ValueError(f'{data_id} is not a valid id.')

        return {
            column.name: getattr(result, column.name)
            for column in result.__table__.columns
        } if as_dict else result
