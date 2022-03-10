"""Application config file"""


class Config:
    # SQLAlchemy parameters
    # SQLALCHEMY_DATABASE_URI = ""
    SQLALCHEMY_RECORD_QUERIES = False

    # App state
    DEBUG = False
    TESTING = False

    PREFERRED_URL_SCHEME = 'https'

    # Logging
    LOGGER_LEVEL = 'INFO'

    # General settings
    TEMPLATES_AUTO_RELOAD = None
    SESSION_COOKIE_SECURE = True

    # API parameters
    API_TITLE = "Monitoring project API"
    API_VERSION = 0.1
    OPENAPI_VERSION = '3.0.2'
    OPENAPI_JSON_PATH = "api-spec.json"
    OPENAPI_URL_PREFIX = "/"
    OPENAPI_REDOC_PATH = "/"
    OPENAPI_REDOC_URL = (
        "https://cdn.jsdelivr.net/npm/redoc@next/bundles/redoc.standalone.js"
    )
    OPENAPI_RAPIDOC_PATH = "/rapidoc"
    OPENAPI_RAPIDOC_URL = "https://unpkg.com/rapidoc/dist/rapidoc-min.js"

    # Flask-APScheduler config
    SCHEDULER_API_ENABLED = True
    AUTO_CHECK_INTERVAL = 30  # Minutes
    AUTO_CHECK_EXECUTE_AFTER = 3  # Seconds (for the first execution)
    SCHEDULER_TIMEZONE = "Europe/Paris"

    # Secret Key
    ################
    # See: https://flask.palletsprojects.com/en/1.0.x/quickstart/#sessions
    # Use -> python -c "import os; print(os.urandom(16))" to generate one
    ################
    SECRET_KEY = '(\x80\x04\xe6{h\xbc\xb4\xec\x0b\x8e#~\xd2\nx'


class ProductionConfig(Config):
    SCHEDULER_EXECUTORS = {
        "default": {
            "type": "threadpool",
            "max_workers": 20
        }
    }


class DevelopmentConfig(Config):
    DEBUG = True

    LOGGER_LEVEL = 'DEBUG'
    PREFERRED_URL_SCHEME = 'http'

    TEMPLATES_AUTO_RELOAD = True
    SESSION_COOKIE_SECURE = False

    SQLALCHEMY_RECORD_QUERIES = True
    SQLALCHEMY_ECHO = True
