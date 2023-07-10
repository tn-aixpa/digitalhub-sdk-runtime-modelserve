package it.smartcommunitylabdhub.core.components.fsm;

import java.io.IOException;
import java.io.Serializable;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.UUID;
import java.util.function.BiConsumer;
import java.util.function.BiFunction;
import java.util.function.Consumer;
import java.util.stream.Collectors;

import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
public class StateMachine<S, E, C> implements Serializable {
    private String uuid;
    private S currentState;
    private S errorState;
    private Map<S, State<S, E, C>> states;
    private Map<E, BiConsumer<?, C>> eventListeners;
    private BiConsumer<S, C> stateChangeListener;
    private C context;

    public StateMachine() {
    }

    public StateMachine(S initialState, C initialContext) {
        this.uuid = UUID.randomUUID().toString();
        this.currentState = initialState;
        this.errorState = null;
        this.states = new HashMap<>();
        this.eventListeners = new HashMap<>();
        this.context = initialContext;
    }

    public static <S, E, C> Builder<S, E, C> builder(S initialState, C initialContext) {
        return new Builder<>(initialState, initialContext);
    }

    public String serialize() throws IOException {
        return null;
    }

    public static <S, E, C> StateMachine<S, E, C> deserialize(String data) throws IOException {
        return null;
    }

    // Builder
    public static class Builder<S, E, C> implements Serializable {
        private S currentState;
        private S errorState;
        private Map<S, State<S, E, C>> states;
        private Map<E, BiConsumer<?, C>> eventListeners;
        private BiConsumer<S, C> stateChangeListener;
        private C context;

        public Builder(S initialState, C initialContext) {
            this.currentState = initialState;
            this.context = initialContext;
            this.states = new HashMap<>();
            this.eventListeners = new HashMap<>();
        }

        public Builder<S, E, C> withState(S state, State<S, E, C> stateDefinition) {
            states.put(state, stateDefinition);
            return this;
        }

        public Builder<S, E, C> withErrorState(S errorState, State<S, E, C> stateDefinition) {
            this.errorState = errorState;

            // Add the error state to the states map if it doesn't exist
            if (!states.containsKey(errorState)) {
                states.put(errorState, stateDefinition);
            }
            return this;
        }

        public <T> Builder<S, E, C> withEventListener(E eventName, BiConsumer<T, C> listener) {
            eventListeners.put(eventName, listener);
            return this;
        }

        public Builder<S, E, C> withStateChangeListener(BiConsumer<S, C> listener) {
            stateChangeListener = listener;
            return this;
        }

        public Builder<S, E, C> withExternalEventListener(E eventName, Consumer<Optional<?>> listener) {
            eventListeners.put(eventName, (input, context) -> listener.accept((Optional<?>) input));
            return this;
        }

        public StateMachine<S, E, C> build() {
            StateMachine<S, E, C> stateMachine = new StateMachine<>(currentState, context);
            stateMachine.states = states;
            stateMachine.errorState = errorState;
            stateMachine.eventListeners = eventListeners;
            stateMachine.stateChangeListener = stateChangeListener;
            return stateMachine;
        }

    }

    // Logic
    @SuppressWarnings("unchecked")
    public <T, R> Optional<T> processEvent(E eventName, Optional<?> input) {
        State<S, E, C> currentStateDefinition = states.get(currentState);
        if (currentStateDefinition == null) {
            throw new IllegalStateException("Invalid current state: " + currentState + " : " + this.getUuid());
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
                    throw new IllegalStateException("Invalid next state: " + nextState + " : " + this.getUuid());
                }

                // Entry action of the next state
                nextStateDefinition.getEntryAction().ifPresent(action -> action.accept(context));

                // Notify event listener
                notifyEventListeners(eventName, input.orElse(null));

                // set new state
                currentState = nextState;

                // Notify state change listener
                notifyStateChangeListener(currentState);

                Optional<T> result = (Optional<T>) nextStateDefinition.getInternalLogic()
                        .map(internalFunc -> applyInternalFunc(
                                (inputValue, contextValue, stateMachineValue) -> internalFunc.applyLogic(inputValue,
                                        contextValue, stateMachineValue),
                                input.orElse(null))

                        ).orElse(Optional.empty());

                // Apply auto transition passing the input
                List<Transaction<S, E, C>> autoTransactions = nextStateDefinition.getTransactions()
                        .entrySet().stream().filter(entry -> entry.getValue().isAuto())
                        .map(Map.Entry::getValue).collect(Collectors.toList());
                for (Transaction<S, E, C> autoTransaction : autoTransactions) {
                    if (autoTransaction.getGuard().test(result, context)) {
                        processEvent(autoTransaction.getEvent(), input);
                    }
                }
                return result;
            } else {
                System.out.println("Guard condition not met for transaction: " + transaction + " : " + this.getUuid());
                // Handle error scenario
                return (Optional<T>) handleTransactionError(transaction, input);
            }
        } else {
            System.out.println("Invalid transaction for event: "
                    + eventName
                    + " : "
                    + this.getUuid() + "\n"
                    + "Current state : " + currentState.toString());
            // Handle error scenario
            return (Optional<T>) handleInvalidTransactionError(eventName, input);
        }
    }

    private <T> Optional<T> applyInternalFunc(StateLogic<S, E, C, T> stateLogic, Object value) {
        return stateLogic.applyLogic(value, context, this);
    }

    private Optional<?> handleTransactionError(Transaction<S, E, C> transaction, Optional<?> input) {
        if (errorState != null) {
            // Transition to the error state
            currentState = errorState;
            State<S, E, C> errorStateDefinition = states.get(errorState);
            if (errorStateDefinition != null) {
                // Execute error logic
                return errorStateDefinition.getInternalLogic()
                        .map(errorLogic -> applyErrorLogic(errorLogic, input.orElse(null))).orElse(Optional.empty());
            } else {
                throw new IllegalStateException("Invalid error state: " + errorState + " : " + this.getUuid());
            }
        } else {
            throw new IllegalStateException("Error state not set" + " : " + this.getUuid());
        }
    }

    private Optional<?> handleInvalidTransactionError(E eventName, Optional<?> input) {
        if (errorState != null) {
            // Transition to the error state
            currentState = errorState;
            State<S, E, C> errorStateDefinition = states.get(errorState);
            if (errorStateDefinition != null) {
                // Execute error logic
                return errorStateDefinition.getInternalLogic()
                        .map(errorLogic -> applyErrorLogic(errorLogic, input.orElse(null))).orElse(Optional.empty());

            } else {
                throw new IllegalStateException("Invalid error state: " + errorState + " : " + this.getUuid());
            }
        } else {
            throw new IllegalStateException("Error state not set" + " : " + this.getUuid());
        }
    }

    @SuppressWarnings("unchecked")
    private Optional<?> applyErrorLogic(Object errorLogic, Object value) {
        BiFunction<Object, C, ?> errorFunction = (arg0, arg1) -> ((BiFunction<Object, C, ?>) errorLogic).apply(arg0,
                arg1);
        return Optional.of(errorFunction.apply(value, context));
    }

    @SuppressWarnings("unchecked")
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
