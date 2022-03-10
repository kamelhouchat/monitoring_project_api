"""General conf for tests."""

from pathlib import Path

import pytest
from dotenv import load_dotenv

from monitoring_project_api import create_app
from monitoring_project_api.config import Config
from monitoring_project_api.extensions.database import db
from monitoring_project_api.models import Data

load_dotenv(Path(__file__).parent / ".env")


class TestingConfig(Config):
    TESTING = True
    SCHEDULER_API_ENABLED = True
    LOGGER_LEVEL = 'CRITICAL'


@pytest.fixture
def database(tmpdir):
    """Configure a test database

    This function is meant to be used in a pytest fixture. It configures the
    test database by creating all tables, yields the ``db`` accessor set to
    operate on this database, then does the cleanup when the test is done.
    """
    db.set_sqla_db_url(f"sqlite:///{tmpdir}/test.sqlite")
    db.sqla_create_all()
    yield db
    db.session.remove()
    # Destroy DB engine
    db.dispose()


@pytest.fixture(params=(TestingConfig,))
def app(request, database):
    class TestingAppConfig(request.param):
        SQLALCHEMY_DATABASE_URI = database.url

    yield create_app(TestingAppConfig)


@pytest.fixture
def client(app):
    yield app.test_client()


@pytest.fixture(name='dummy_id')
def dummy_id():
    from random import randrange
    return randrange(10000)


@pytest.fixture
def generate_data(database, request):
    marker_data_quantity = request.node.get_closest_marker("data_quantity")
    data_quantity = marker_data_quantity.kwargs['quantity'] \
        if marker_data_quantity is not None else 1
    marker_data_information = request.node.get_closest_marker(
        "data_information")
    data_information = marker_data_information.kwargs if \
        marker_data_information is not None else dict()

    added_data = []
    for _ in range(data_quantity):
        item = Data(
            path=data_information.get('path', "https://dymmy_url.com")
        )
        database.session.add(item)
        database.session.commit()
        added_data.append(item.id)

    return added_data
