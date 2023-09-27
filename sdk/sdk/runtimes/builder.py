"""
Runtime factory module.
"""
from __future__ import annotations

import typing

from sdk.runtimes.registry import REGISTRY_RUNTIMES

if typing.TYPE_CHECKING:
    from sdk.entities.run.entity import Run
    from sdk.runtimes.objects.base import Runtime


class RuntimeBuilder:
    """
    Runtime builder class.
    """

    def build(self, run: Run) -> Runtime:
        """
        Build runtimes.

        Returns
        -------
        dict
            Runtimes.
        """
        framework, action = run.get_function_and_task()
        try:
            return REGISTRY_RUNTIMES.get(framework)[action](run)
        except TypeError:
            raise ValueError(f"Unkwnon framewrok '{framework}'")
        except KeyError:
            raise ValueError(
                f"Invalid operation '{action}' for framewrok '{framework}'"
            )


def build_runtime(run: Run) -> Runtime:
    """
    Wrapper for RuntimeBuilder.build.

    Parameters
    ----------
    run: dict
        Run object.

    Returns
    -------
    Runtime
        Runtime instance.
    """
    return runtime_builder.build(run)


runtime_builder = RuntimeBuilder()
