from typing import Any

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Result, text as SQLQuery
from sqlalchemy.exc import IntegrityError

sqla = SQLAlchemy()


def try_commit() -> None:
    try:
        sqla.session.commit()
    except IntegrityError:
        sqla.session.rollback()
        raise


def callproc(querystring: str) -> Result[Any]:
    sql = SQLQuery(querystring)
    result = sqla.session.execute(sql)
    return result
