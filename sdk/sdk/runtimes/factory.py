"""
Runtime factory module.
"""
from __future__ import annotations

import typing

from sdk.runtimes.registry import REGISTRY_RUNTIMES

if typing.TYPE_CHECKING:
    from sdk.runtimes.objects.base import Runtime


def get_runtime(run: dict) -> Runtime:
    """
    Get runtime instance by framework and operation.

    Parameters
    ----------
    run: dict
        Run object.

    Returns
    -------
    Runtime
        Runtime instance.
    """
    framework, action = run.get_function_and_task()
    try:
        return REGISTRY_RUNTIMES.get(framework)[action](run)
    except TypeError:
        raise ValueError(f"Unkwnon framewrok '{framework}'")
    except KeyError:
        raise ValueError(f"Invalid operation '{action}' for framewrok '{framework}'")
