from . import urlshort  # import the blueprint object
from flask import Flask


def create_app(test_config=None):  # test_config is used for testing
    # create an instance of the Flask class
    app = Flask(__name__)
    app.secret_key = 'someRandomStrongKey'  # used to encrypt the session cookie

    app.register_blueprint(urlshort.bp)  # register the blueprint object

    return app
