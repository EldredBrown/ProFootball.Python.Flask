from app.data.models.season import Season


def create_season(**kwargs) -> Season:
    _validate_key_is_in_kwargs('year', **kwargs)

    return Season(**kwargs)


def _validate_key_is_in_kwargs(key, **kwargs):
    if key not in kwargs:
        raise ValueError(f"{str.capitalize(key)} is required.")
