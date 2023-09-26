REGISTRY_RUNTIMES_BUILD = {}
REGISTRY_RUNTIMES_JOB = {}
try:
    from sdk.runtimes.objects.job.dbt import RuntimeJobDBT

    REGISTRY_RUNTIMES_JOB["dbt"] = RuntimeJobDBT
except ImportError:
    ...
