package it.smartcommunitylabdhub.core.components.fsm;

import java.util.*;
import java.util.function.Function;
import java.util.function.Predicate;

public class StateMachine<S, E, R> {
    private S initialState;
    private S currentState;
    private Map<S, Map<E, Transition<S, E, R>>> transitions;
    private Map<S, Transition<S, E, R>> autoTransitions;
    private Map<E, List<ChangeListener<S, E>>> eventListeners;

    public StateMachine(S initialState) {
        this.initialState = initialState;
        this.currentState = initialState;
        this.transitions = new HashMap<>();
        this.autoTransitions = new HashMap<>();
        this.eventListeners = new HashMap<>();
    }

    public void addTransition(S fromState, E event, S toState, Predicate<S> condition, Function<S, R> logic) {
        if (fromState == null || event == null || toState == null || condition == null || logic == null) {
            throw new IllegalArgumentException("Invalid transition arguments");
        }

        Transition<S, E, R> transition = new Transition<>(fromState, event, toState, condition, logic);
        transitions.computeIfAbsent(fromState, k -> new HashMap<>()).put(event, transition);
    }

    public void addAutoTransition(S state, S toState, Predicate<S> condition, Function<S, R> logic) {
        if (state == null || toState == null || condition == null || logic == null) {
            throw new IllegalArgumentException("Invalid auto-transition arguments");
        }

        Transition<S, E, R> autoTransition = new Transition<>(state, null, toState, condition, logic);
        autoTransitions.put(state, autoTransition);
    }

    public void processEvent(E event) {
        Map<E, Transition<S, E, R>> eventTransitions = transitions.get(currentState);
        if (eventTransitions != null) {
            Transition<S, E, R> transition = eventTransitions.get(event);
            if (transition != null && transition.getCondition().test(currentState)) {
                S nextState = transition.getToState();
                System.out.println("Transition: " + currentState + " -> " + nextState);
                Function<S, R> logic = transition.getLogic();
                if (logic != null) {
                    R result = logic.apply(currentState);
                    nextState = applyResultToNextState(nextState, result);
                }
                notifyListeners(currentState, nextState, event);
                currentState = nextState;
            } else {
                throw new IllegalArgumentException("Invalid transition: " + currentState + " -> " + event);
            }
        } else {
            throw new IllegalArgumentException("Invalid state: " + currentState);
        }

        processAutoTransitions(currentState); // Process auto transitions after the current transition
    }

    private S applyResultToNextState(S nextState, R result) {
        if (result != null) {
            Map<E, Transition<S, E, R>> eventTransitions = transitions.get(nextState);
            if (eventTransitions != null) {
                Transition<S, E, R> transition = eventTransitions.get(result);
                if (transition != null && transition.getCondition().test(nextState)) {
                    nextState = transition.getToState();
                }
            }
        }

        return nextState;
    }

    private void processAutoTransitions(S currentState) {
        boolean hasAutoTransitions = false;
        do {
            hasAutoTransitions = false;
            Transition<S, E, R> autoTransition = autoTransitions.get(currentState);
            if (autoTransition != null && autoTransition.getCondition().test(currentState)) {
                S nextState = autoTransition.getToState();
                System.out.println("Auto Transition: " + currentState + " -> " + nextState);
                Function<S, R> logic = autoTransition.getLogic();
                if (logic != null) {
                    R result = logic.apply(currentState);
                    nextState = applyResultToNextState(nextState, result);
                }
                notifyListeners(currentState, nextState, null);
                currentState = nextState;
                hasAutoTransitions = true;
            }
        } while (hasAutoTransitions);
    }

    public void addChangeListener(E event, ChangeListener<S, E> listener) {
        if (event == null || listener == null) {
            throw new IllegalArgumentException("Invalid change listener arguments");
        }

        eventListeners.computeIfAbsent(event, k -> new ArrayList<>()).add(listener);
    }

    private void notifyListeners(S fromState, S toState, E event) {
        List<ChangeListener<S, E>> listeners = eventListeners.get(event);
        if (listeners != null) {
            for (ChangeListener<S, E> listener : listeners) {
                listener.onStateChange(fromState, toState, event);
            }
        }
    }

    @Override
    public boolean equals(Object obj) {
        if (this == obj) {
            return true;
        }
        if (obj == null || getClass() != obj.getClass()) {
            return false;
        }
        StateMachine<?, ?, ?> other = (StateMachine<?, ?, ?>) obj;
        return Objects.equals(initialState, other.initialState)
                && Objects.equals(currentState, other.currentState)
                && Objects.equals(transitions, other.transitions)
                && Objects.equals(autoTransitions, other.autoTransitions)
                && Objects.equals(eventListeners, other.eventListeners);
    }

    @Override
    public int hashCode() {
        return Objects.hash(initialState, currentState, transitions, autoTransitions, eventListeners);
    }

    // Add getter methods for private fields

    public S getInitialState() {
        return initialState;
    }

    public S getCurrentState() {
        return currentState;
    }

    public Map<S, Map<E, Transition<S, E, R>>> getTransitions() {
        return transitions;
    }

    public Map<S, Transition<S, E, R>> getAutoTransitions() {
        return autoTransitions;
    }

    public Map<E, List<ChangeListener<S, E>>> getEventListeners() {
        return eventListeners;
    }
}
