package it.smartcommunitylabdhub.core.components.fsm;

import java.io.Serializable;
import java.util.HashMap;
import java.util.Map;
import java.util.Optional;
import java.util.function.BiFunction;
import java.util.function.Consumer;

public class State<S, E, C> implements Serializable {

    private Optional<Consumer<C>> entryAction;
    private Optional<Consumer<C>> exitAction;
    private Optional<BiFunction<?, C, ?>> internalLogic;
    private Map<E, Transaction<S, E, C>> transactions;

    public State() {
        this.internalLogic = Optional.empty();
        this.exitAction = Optional.empty();
        this.entryAction = Optional.empty();
        this.transactions = new HashMap<>();
    }

    public Optional<BiFunction<?, C, ?>> getInternalLogic() {
        return internalLogic;
    }

    public <T> void setInternalLogic(BiFunction<T, C, ?> internalLogic) {
        this.internalLogic = Optional.ofNullable(internalLogic);
    }

    public void addTransaction(Transaction<S, E, C> transaction) {
        transactions.put(transaction.getEvent(), transaction);
    }

    public Map<E, Transaction<S, E, C>> getTransactions() {
        return transactions;
    }

    public Optional<Consumer<C>> getEntryAction() {
        return entryAction;
    }

    public <T> void setEntryAction(Consumer<C> entryAction) {
        this.entryAction = Optional.of(entryAction);
    }

    public Optional<Consumer<C>> getExitAction() {
        return exitAction;
    }

    public void setExitAction(Consumer<C> exitAction) {
        this.exitAction = Optional.of(exitAction);
    }
}