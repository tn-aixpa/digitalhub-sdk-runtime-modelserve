from __future__ import annotations


def serve_sklearn(**kwargs) -> str:
    """
    Serve sklearn function.

    Parameters
    ----------
    **kwargs
        The serve arguments.

    Returns
    -------
    str
        The endpoint where the model is served.
    """
    return "sklearn"


def config_sklearn(**kwargs) -> dict:
    """
    Configure sklearn function.

    Parameters
    ----------
    **kwargs
        The configure arguments.

    Returns
    -------
    dict
        The function configuration.
    """
    return {}
