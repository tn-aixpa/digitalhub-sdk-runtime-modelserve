/**
 * State.java
 *
 * This class represents a state in the State Machine. It contains information about the entry
 * action, exit action, internal logic, and transactions associated with the state.
 *
 * @param <S> The type of the states.
 * @param <E> The type of the events.
 * @param <C> The type of the context.
 */

package it.smartcommunitylabdhub.core.components.fsm;

import java.util.HashMap;
import java.util.Map;
import java.util.Optional;

public class State<S, E, C> {
    private Optional<StateLogic<S, E, C, ?>> internalLogic;
    private Map<E, Transaction<S, E, C>> transactions;
    private Context<C> context;

    public State() {
        internalLogic = Optional.empty();
        transactions = new HashMap<>();
        context = new Context<C>(Optional.empty());
    }

    /**
     * Add a context associated with this state.
     *
     * @param context The context to add.
     */
    public void setContext(Context<C> context) {
        this.context = context;
    }

    /**
     * Return an optionl context of the state
     * 
     * @return context The context of the state.
     */
    public Context<C> getContext() {
        return context;
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
     * @param <T> The type of the result from the internal logic.
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
     * @return The map of transactions, where the key is the event and the value is the
     *         corresponding transaction.
     */
    public Map<E, Transaction<S, E, C>> getTransactions() {
        return transactions;
    }

}
