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

    public E getEvent() {
        return event;
    }

    public S getNextState() {
        return nextState;
    }

    public BiPredicate<Optional<?>, C> getGuard() {
        return guard;
    }

    public boolean isAuto() {
        return isAuto;
    }

    public void setAuto(boolean isAuto) {
        this.isAuto = isAuto;
    }
}