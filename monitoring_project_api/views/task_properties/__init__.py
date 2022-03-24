"""Task view"""

from .routes import bp


def register_blueprints(api):
    api.register_blueprint(bp)
