import pytest

from app.data.models.league_season import LeagueSeason


def test_validate_not_empty_when_league_id_is_none_should_raise_value_error():
    # Arrange
    # Act
    with pytest.raises(ValueError) as err:
        test_league_season = LeagueSeason(league_id=None)

    # Assert
    assert isinstance(err.value, ValueError)
    assert err.value.args[0] == "league_id is required."


def test_validate_not_empty_when_league_id_is_zero_should_not_raise_value_error():
    # Arrange
    err = None

    # Act
    try:
        test_league_season = LeagueSeason(league_id=0)
    except ValueError as err:
        pass

    # Assert
    assert err is None


def test_validate_not_empty_when_league_id_is_greater_than_zero_should_not_raise_value_error():
    # Arrange
    err = None

    # Act
    try:
        test_league_season = LeagueSeason(league_id=1)
    except ValueError as err:
        pass

    # Assert
    assert err is None


def test_validate_not_empty_when_season_id_is_none_should_raise_value_error():
    # Arrange
    # Act
    with pytest.raises(ValueError) as err:
        test_league_season = LeagueSeason(league_id=1, season_id=None)

    # Assert
    assert isinstance(err.value, ValueError)
    assert err.value.args[0] == "season_id is required."


def test_validate_not_empty_when_season_id_is_zero_should_not_raise_value_error():
    # Arrange
    err = None

    # Act
    try:
        test_league_season = LeagueSeason(league_id=1, season_id=0)
    except ValueError as err:
        pass

    # Assert
    assert err is None


def test_validate_not_empty_when_season_id_is_greater_than_zero_should_not_raise_value_error():
    # Arrange
    err = None

    # Act
    try:
        test_league_season = LeagueSeason(league_id=1, season_id=1)
    except ValueError as err:
        pass

    # Assert
    assert err is None
