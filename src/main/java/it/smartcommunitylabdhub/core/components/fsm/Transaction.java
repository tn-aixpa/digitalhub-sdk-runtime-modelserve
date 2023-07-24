/**
 * Transaction.java
 *
 * This class represents a transition in the State Machine. It defines the event, next state, guard, and auto-flag
 * for the transition.
 *
 * @param <S> The type of the states.
 * @param <E> The type of the events.
 * @param <C> The type of the context.
 */

package it.smartcommunitylabdhub.core.components.fsm;

import java.util.Optional;
import java.util.function.BiPredicate;

public class Transaction<S, E, C> {
    private E event;
    private S nextState;
    private BiPredicate<Optional<?>, C> guard;
    private boolean isAuto;

    public Transaction(E event, S nextState, BiPredicate<Optional<?>, C> guard, boolean isAuto) {
        this.event = event;
        this.nextState = nextState;
        this.guard = guard;
        this.isAuto = isAuto;
    }

    /**
     * Get the event associated with this transaction.
     *
     * @return The event.
     */
    public E getEvent() {
        return event;
    }

    /**
     * Get the next state to transition to.
     *
     * @return The next state.
     */
    public S getNextState() {
        return nextState;
    }

    /**
     * Get the guard function associated with this transaction.
     *
     * @return The guard function.
     */
    public BiPredicate<Optional<?>, C> getGuard() {
        return guard;
    }

    /**
     * Check if this transaction is an auto-transition.
     *
     * @return True if it is an auto-transition, false otherwise.
     */
    public boolean isAuto() {
        return isAuto;
    }

    /**
     * Set the auto flag for this transaction.
     *
     * @param isAuto True if it is an auto-transition, false otherwise.
     */
    public void setAuto(boolean isAuto) {
        this.isAuto = isAuto;
    }
}