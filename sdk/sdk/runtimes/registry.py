REGISTRY_RUNTIMES_BUILD = {}
REGISTRY_RUNTIMES_PERFORM = {}
try:
    from sdk.runtimes.objects.perform.dbt import RuntimePerformDBT

    REGISTRY_RUNTIMES_PERFORM["dbt"] = RuntimePerformDBT
except ImportError:
    ...
