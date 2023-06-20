package it.smartcommunitylabdhub.core.components.fsm;

import java.util.function.Function;
import java.util.function.Predicate;

public class Transition<S, E, R> {
    private S fromState;
    private E event;
    private S toState;
    private Predicate<S> condition;
    private Function<S, R> logic;

    public Transition(S fromState, E event, S toState, Predicate<S> condition, Function<S, R> logic) {
        this.fromState = fromState;
        this.event = event;
        this.toState = toState;
        this.condition = condition;
        this.logic = logic;
    }

    public S getFromState() {
        return fromState;
    }

    public E getEvent() {
        return event;
    }

    public S getToState() {
        return toState;
    }

    public Predicate<S> getCondition() {
        return condition;
    }

    public Function<S, R> getLogic() {
        return logic;
    }
}