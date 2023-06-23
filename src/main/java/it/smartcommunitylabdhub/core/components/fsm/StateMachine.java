package it.smartcommunitylabdhub.core.components.fsm;

import java.io.Serializable;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.function.BiConsumer;
import java.util.function.BiFunction;
import java.util.function.Consumer;
import java.util.stream.Collectors;

public class StateMachine<S, E, C> implements Serializable {
    private S currentState;
    private S errorState;
    private Map<S, State<S, E, C>> states;
    private Map<E, BiConsumer<?, C>> eventListeners;
    private BiConsumer<S, C> stateChangeListener;
    private C context;

    public StateMachine(S initialState, C initialContext) {
        this.currentState = initialState;
        this.errorState = null;
        this.states = new HashMap<>();
        this.eventListeners = new HashMap<>();
        this.context = initialContext;
    }

    // Builder
    public void addState(S state, State<S, E, C> stateDefinition) {
        states.put(state, stateDefinition);
    }

    public void setErrorState(S errorState, State<S, E, C> stateDefinition) {
        this.errorState = errorState;

        // Add the error state to the states map if it doesn't exist
        if (!states.containsKey(errorState)) {
            states.put(errorState, stateDefinition);
        }
    }

    public <T> void addEventListener(E eventName, BiConsumer<T, C> listener) {
        eventListeners.put(eventName, listener);
    }

    public void setStateChangeListener(BiConsumer<S, C> listener) {
        stateChangeListener = listener;
    }

    public void addExternalEventListener(E eventName, Consumer<Optional<?>> listener) {
        eventListeners.put(eventName, (input, context) -> listener.accept((Optional<?>) input));
    }

    // Logic
    public <T, R> void processEvent(E eventName, Optional<?> input) {
        State<S, E, C> currentStateDefinition = states.get(currentState);
        if (currentStateDefinition == null) {
            throw new IllegalStateException("Invalid current state: " + currentState);
        }

        // Exit action of the current state
        currentStateDefinition.getExitAction().ifPresent(action -> action.accept(context));

        Optional<Transaction<S, E, C>> matchingTransaction = Optional.ofNullable(
                currentStateDefinition.getTransactions().get(eventName));

        if (matchingTransaction.isPresent()) {
            Transaction<S, E, C> transaction = matchingTransaction.get();
            if (transaction.getGuard().test(input, context)) {
                S nextState = transaction.getNextState();
                State<S, E, C> nextStateDefinition = states.get(nextState);
                if (nextStateDefinition == null) {
                    throw new IllegalStateException("Invalid next state: " + nextState);
                }

                // Entry action of the next state
                nextStateDefinition.getEntryAction().ifPresent(action -> action.accept(context));

                // Notify event listener
                notifyEventListeners(eventName, input.orElse(null));

                // set new state
                currentState = nextState;

                // Notify state change listener
                notifyStateChangeListener(currentState);

                nextStateDefinition.getInternalLogic().ifPresent(internalFunc -> {
                    Optional<?> result = input
                            .flatMap(value -> applyInternalFunc((BiFunction<?, C, Optional<T>>) internalFunc, value));
                });

                // Apply auto transition passing the input
                List<Transaction<S, E, C>> autoTransactions = nextStateDefinition.getTransactions()
                        .entrySet().stream().filter(entry -> entry.getValue().isAuto())
                        .map(Map.Entry::getValue).collect(Collectors.toList());
                for (Transaction<S, E, C> autoTransaction : autoTransactions) {
                    if (autoTransaction.getGuard().test(input, context)) {
                        processEvent(autoTransaction.getEvent(), input);
                    }
                }
            } else {
                System.out.println("Guard condition not met for transaction: " + transaction);
                // Handle error scenario
                handleTransactionError(transaction, input);
            }
        } else {
            System.out.println("Invalid transaction for event: " + eventName);
            // Handle error scenario
            handleInvalidTransactionError(eventName, input);
        }
    }

    private <T> Optional<T> applyInternalFunc(BiFunction<?, C, Optional<T>> internalFunc, Object value) {
        @SuppressWarnings("unchecked")
        BiFunction<Object, C, Optional<T>> func = (BiFunction<Object, C, Optional<T>>) internalFunc;
        return func.apply(value, context);
    }

    private void handleTransactionError(Transaction<S, E, C> transaction, Optional<?> input) {
        if (errorState != null) {
            // Transition to the error state
            currentState = errorState;
            State<S, E, C> errorStateDefinition = states.get(errorState);
            if (errorStateDefinition != null) {
                // Execute error logic
                errorStateDefinition.getInternalLogic().ifPresent(errorLogic -> {
                    applyErrorLogic(errorLogic, input.orElse(null));
                });
            } else {
                throw new IllegalStateException("Invalid error state: " + errorState);
            }
        } else {
            throw new IllegalStateException("Error state not set");
        }
    }

    private void handleInvalidTransactionError(E eventName, Optional<?> input) {
        if (errorState != null) {
            // Transition to the error state
            currentState = errorState;
            State<S, E, C> errorStateDefinition = states.get(errorState);
            if (errorStateDefinition != null) {
                // Execute error logic
                errorStateDefinition.getInternalLogic().ifPresent(errorLogic -> {
                    applyErrorLogic(errorLogic, input.orElse(null));
                });
            } else {
                throw new IllegalStateException("Invalid error state: " + errorState);
            }
        } else {
            throw new IllegalStateException("Error state not set");
        }
    }

    private void applyErrorLogic(Object errorLogic, Object value) {
        BiFunction<Object, C, ?> errorFunction = (arg0, arg1) -> ((BiFunction<Object, C, ?>) errorLogic).apply(arg0,
                arg1);
        errorFunction.apply(value, context);
    }

    private <T> void notifyEventListeners(E eventName, T input) {
        BiConsumer<T, C> listener = (BiConsumer<T, C>) eventListeners.get(eventName);
        if (listener != null) {
            listener.accept(input, context);
        }
    }

    private void notifyStateChangeListener(S newState) {
        if (stateChangeListener != null) {
            stateChangeListener.accept(newState, context);
        }
    }
}
