from app.data.models.team import Team


def create_team(**kwargs) -> Team:
    view_model_map = {
        'id':   'id',
        'name': 'name',
    }

    model_kwargs = dict()
    for key in kwargs.keys():
        if key not in view_model_map:
            raise KeyError(f"{key} is invalid.")

        value = kwargs.get(key)
        model_kwargs[view_model_map[key]] = value

    return Team(**model_kwargs)
