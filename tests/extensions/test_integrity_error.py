"""Test integrity error"""

import flask
from sqlalchemy.exc import IntegrityError

from monitoring_project_api.extensions import Api
from monitoring_project_api.extensions import Blueprint


class TestIntegrityError:

    def test_catch_integrity_error(self):
        app = flask.Flask('Test')
        api = Api(
            app,
            spec_kwargs={
                "title": "Test API",
                "version": "1",
                "openapi_version": "3"
            }
        )

        bp = Blueprint('Test', __name__, url_prefix='/test')

        @bp.route('/test_integrity')
        @bp.response(200)
        @bp.catch_integrity_error
        def test_integrity():
            raise IntegrityError(None, None, None)

        api.register_blueprint(bp)
        client = app.test_client()

        resp = client.get('/test/test_integrity')
        assert resp.status_code == 409
