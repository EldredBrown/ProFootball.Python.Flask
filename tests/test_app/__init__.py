from flask import Flask

from app.data.sqla import sqla


def create_app():
    app = Flask(__name__)

    app.config.from_mapping(
        SECRET_KEY='secretkey',
        SQLALCHEMY_DATABASE_URI='sqlite:///test_db/test_db.sqlite3',
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        DEBUG=True
    )

    sqla.init_app(app)

    return app
