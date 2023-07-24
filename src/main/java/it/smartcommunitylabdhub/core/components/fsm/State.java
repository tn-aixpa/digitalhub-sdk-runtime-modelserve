/**
 * State.java
 *
 * This class represents a state in the State Machine. It contains information about the entry action, exit action,
 * internal logic, and transactions associated with the state.
 *
 * @param <S> The type of the states.
 * @param <E> The type of the events.
 * @param <C> The type of the context.
 */

package it.smartcommunitylabdhub.core.components.fsm;

import java.util.HashMap;
import java.util.Map;
import java.util.Optional;
import java.util.function.Consumer;

public class State<S, E, C> {

    private Optional<Consumer<C>> entryAction;
    private Optional<Consumer<C>> exitAction;
    private Optional<StateLogic<S, E, C, ?>> internalLogic;
    private Map<E, Transaction<S, E, C>> transactions;

    public State() {
        this.internalLogic = Optional.empty();
        this.exitAction = Optional.empty();
        this.entryAction = Optional.empty();
        this.transactions = new HashMap<>();
    }

    /**
     * Get the internal logic associated with this state.
     *
     * @return The internal logic as a StateLogic instance.
     */
    public Optional<StateLogic<S, E, C, ?>> getInternalLogic() {
        return internalLogic;
    }

    /**
     * Set the internal logic for this state.
     *
     * @param internalLogic The internal logic as a StateLogic instance.
     * @param <T>           The type of the result from the internal logic.
     */
    public <T> void setInternalLogic(StateLogic<S, E, C, T> internalLogic) {
        this.internalLogic = Optional.ofNullable(internalLogic);
    }

    /**
     * Add a transaction associated with this state.
     *
     * @param transaction The transaction to add.
     */
    public void addTransaction(Transaction<S, E, C> transaction) {
        transactions.put(transaction.getEvent(), transaction);
    }

    /**
     * Get the transactions associated with this state.
     *
     * @return The map of transactions, where the key is the event and the value is
     *         the corresponding transaction.
     */
    public Map<E, Transaction<S, E, C>> getTransactions() {
        return transactions;
    }

    /**
     * Get the entry action associated with this state.
     *
     * @return The entry action as a Consumer instance.
     */
    public Optional<Consumer<C>> getEntryAction() {
        return entryAction;
    }

    /**
     * Set the entry action for this state.
     *
     * @param entryAction The entry action as a Consumer instance.
     * @param <T>         The type of the input for the entry action.
     */
    public void setEntryAction(Consumer<C> entryAction) {
        this.entryAction = Optional.of(entryAction);
    }

    /**
     * Get the exit action associated with this state.
     *
     * @return The exit action as a Consumer instance.
     */
    public Optional<Consumer<C>> getExitAction() {
        return exitAction;
    }

    /**
     * Set the exit action for this state.
     *
     * @param exitAction The exit action as a Consumer instance.
     * @param <T>        The type of the input for the exit action.
     */
    public void setExitAction(Consumer<C> exitAction) {
        this.exitAction = Optional.of(exitAction);
    }
}