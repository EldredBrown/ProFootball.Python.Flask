from unittest.mock import patch

import pytest

from sqlalchemy.exc import IntegrityError

from app.data import sqla as mod


@patch('app.data.sqla.sqla')
def test_try_commit_when_no_integrity_error_caught_should_commit_transaction(fake_sqla):
    # Arrange

    # Act
    try:
        mod.try_commit()
    except IntegrityError:
        assert False

    # Assert
    fake_sqla.session.commit.assert_called_once()


@patch('app.data.sqla.sqla')
def test_try_commit_when_integrity_error_caught_should_rollback_transaction(fake_sqla):
    # Arrange
    fake_sqla.session.commit.side_effect = IntegrityError('statement', 'params', Exception())

    # Act
    with pytest.raises(IntegrityError):
        mod.try_commit()

    # Assert
    fake_sqla.session.rollback.assert_called_once()
