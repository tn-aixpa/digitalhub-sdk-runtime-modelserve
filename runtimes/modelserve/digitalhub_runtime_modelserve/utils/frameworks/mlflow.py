from __future__ import annotations


def serve_mlflow(**kwargs) -> str:
    """
    Serve mlflow function.

    Parameters
    ----------
    **kwargs
        The serve arguments.

    Returns
    -------
    str
        The endpoint where the model is served.
    """
    return "mlflow"


def config_mlflow(**kwargs) -> dict:
    """
    Configure mlflow function.

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
