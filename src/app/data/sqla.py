from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError

sqla = SQLAlchemy()


def try_commit() -> None:
    try:
        sqla.session.commit()
    except IntegrityError:
        sqla.session.rollback()
        raise
