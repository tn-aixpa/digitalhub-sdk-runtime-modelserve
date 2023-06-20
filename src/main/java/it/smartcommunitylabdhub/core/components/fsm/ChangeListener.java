package it.smartcommunitylabdhub.core.components.fsm;

@FunctionalInterface
public interface ChangeListener<S, E> {
    void onStateChange(S fromState, S toState, E event);
}