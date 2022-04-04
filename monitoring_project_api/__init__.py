"""Monitoring project API Flask APP"""

import click
import flask.cli
import sqlalchemy
from flask import Flask
from flask.helpers import get_env

from .extensions import Api
from .extensions import AutoSchema  # noqa
from .extensions import Blueprint  # noqa
from .extensions import SQLCursorPage  # noqa
from .extensions import Schema  # noqa
from .extensions.scheduler.scheduler_manager import scheduler_manager
from .views import register_blueprints

_APP_NAME = 'monitoring_project_api'
DEFAULT_CONFIG_FILE = 'monitoring_project_api.config'
CONFIGS = {
    'production': 'ProductionConfig',
    'development': 'DevelopmentConfig'
}


@click.command()
@flask.cli.with_appcontext
def setup_db():
    from .extensions.database import db

    db.sqla_setup_tables()
    db.session.commit()


def create_app(cfg_class=None):
    app = build_app(cfg_class)
    configure_app(app)

    app.logger.info("Monitoring Project API started !")

    return app


def build_app(cfg_class=None):
    # Initialize Flask App
    app = Flask(_APP_NAME)

    # Configure Flask app
    if cfg_class is None:
        cfg_class = '.'.join((DEFAULT_CONFIG_FILE, CONFIGS[get_env()]))

    app.config.from_object(cfg_class)
    app.config.from_envvar('FLASK_SETTINGS_FILE', silent=True)

    app.logger.debug('Starting...')

    return app


def configure_app(app):
    # Initialize extensions
    app.logger.debug('Initialize extensions ... ')

    # Initialize db
    app.logger.debug('Initialize db ...')
    from .extensions import db_init_app
    db_init_app(app)

    # initialize scheduler
    from .extensions.scheduler import scheduler
    from .extensions.scheduler import events  # noqa
    import logging
    app.logger.debug('Initialize scheduler ...')
    scheduler.init_app(app)
    logging.getLogger("apscheduler").setLevel(logging.INFO)
    with app.app_context():
        from .extensions.scheduler import tasks  # noqa
        if app.config['TESTING'] is not True:
            scheduler.start()

    # Init log folder
    from pathlib import Path
    logging_path = Path(app.config['LOGGING_FILE_PATH'])
    if not logging_path.is_dir():
        logging_path.mkdir(parents=True)

    # Restore old job
    # noinspection PyUnresolvedReferences
    from .models.init_db_values import PROCESSING_METHODS
    try:
        number_of_added_jobs = scheduler_manager(PROCESSING_METHODS.keys(),
                                                 logging_path=logging_path)
        app.logger.debug(f'<Scheduler> : Restore old job '
                         f'{number_of_added_jobs} added jobs')
    except sqlalchemy.exc.OperationalError:
        pass

    # Initialize API
    app.logger.debug('Initialize API ...')
    api = Api()
    api.init_app(app)

    # Register views
    app.logger.debug('Registering views ...')
    register_blueprints(api)

    # Register cli command
    app.logger.debug('Registering cli commands ...')
    app.cli.add_command(setup_db)
