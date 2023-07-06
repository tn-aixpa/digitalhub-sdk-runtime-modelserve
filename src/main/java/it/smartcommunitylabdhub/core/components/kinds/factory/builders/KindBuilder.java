package it.smartcommunitylabdhub.core.components.kinds.factory.builders;

@FunctionalInterface
public interface KindBuilder<I, O> {
    O build(I input);
}
