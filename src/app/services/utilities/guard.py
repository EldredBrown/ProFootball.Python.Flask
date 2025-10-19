def raise_if_none(arg_value: object, param_name: str) -> None:
    """
    Raises a ValueError if the specified arg_value is None.

    :param arg_value: The argument value to check.
    :param param_name: The parameter id to pass to the raised ValueError.

    :return: None

    :raises ValueError: If the specified arg_value is None.
    """
    if arg_value is None:
        raise ValueError(param_name)
