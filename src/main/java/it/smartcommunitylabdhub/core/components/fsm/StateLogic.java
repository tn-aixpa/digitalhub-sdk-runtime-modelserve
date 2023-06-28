package it.smartcommunitylabdhub.core.components.fsm;

import java.util.Optional;

@FunctionalInterface
public interface StateLogic<S, E, C, T> {
    Optional<T> applyLogic(Object input, C context, StateMachine<S, E, C> stateMachine);
}
