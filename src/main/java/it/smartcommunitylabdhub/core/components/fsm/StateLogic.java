/**
 * StateLogic.java
 *
 * This functional interface represents the internal logic of a state in the State Machine.
 *
 * @param <S> The type of the states.
 * @param <E> The type of the events.
 * @param <C> The type of the context.
 * @param <T> The type of the result from applying the logic.
 */

package it.smartcommunitylabdhub.core.components.fsm;

import java.util.Optional;

@FunctionalInterface
public interface StateLogic<S, E, C, T> {
    /**
     * Apply the internal logic of the state.
     *
     * @param input        The input value to apply the logic on.
     * @param context      The context for the state machine.
     * @param stateMachine The state machine instance.
     * @return The optional result from applying the logic.
     */
    Optional<T> applyLogic(Object input, C context, StateMachine<S, E, C> stateMachine);
}
