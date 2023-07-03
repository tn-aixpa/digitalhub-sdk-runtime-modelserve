package it.smartcommunitylabdhub.core.models.builders.kinds.factory;

@FunctionalInterface
public interface KindBuilder<I, O> {
    O build(I input);
}
