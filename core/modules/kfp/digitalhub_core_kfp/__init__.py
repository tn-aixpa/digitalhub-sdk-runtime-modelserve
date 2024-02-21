from digitalhub_core.runtimes.registry import RuntimeRegistry

registry = RuntimeRegistry()
registry.register(
    "digitalhub_core_kfp.runtimes.runtime",
    "RuntimeKFP",
)
