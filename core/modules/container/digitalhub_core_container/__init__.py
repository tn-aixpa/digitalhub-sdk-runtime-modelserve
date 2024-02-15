from digitalhub_core.runtimes.registry import RuntimeRegistry

registry = RuntimeRegistry()
registry.register(
    "digitalhub_core_container.runtimes.runtime",
    "RuntimeContainer",
)
