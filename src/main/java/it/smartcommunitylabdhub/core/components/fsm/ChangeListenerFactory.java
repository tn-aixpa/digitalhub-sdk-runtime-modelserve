package it.smartcommunitylabdhub.core.components.fsm;

public interface ChangeListenerFactory<S, E> {
    ChangeListener<S, E> createListener();
}