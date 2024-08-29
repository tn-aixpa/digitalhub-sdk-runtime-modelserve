from __future__ import annotations


def serve_huggingface(**kwargs) -> str:
    """
    Serve huggingface function.

    Parameters
    ----------
    **kwargs
        The serve arguments.

    Returns
    -------
    str
        The endpoint where the model is served.
    """
    return "huggingface"


def config_huggingface(**kwargs) -> dict:
    """
    Configure huggingface function.

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
