package it.smartcommunitylabdhub.core.components.kinds.factory.workflows;

@FunctionalInterface
public interface KindWorkflow<I, O> {
    O build(I input);
}
