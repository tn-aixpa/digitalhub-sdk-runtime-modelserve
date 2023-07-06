package it.smartcommunitylabdhub.core.components.kinds.factory.publishers;

@FunctionalInterface
public interface KindPublisher<I, O> {
    O publish(I input);
}
