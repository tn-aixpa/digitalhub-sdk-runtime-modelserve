REGISTRY_RUNTIMES = {}
try:
    from sdk.runtimes.objects.dbt import DBTRuntime

    REGISTRY_RUNTIMES["dbt"] = DBTRuntime
except ImportError:
    ...
