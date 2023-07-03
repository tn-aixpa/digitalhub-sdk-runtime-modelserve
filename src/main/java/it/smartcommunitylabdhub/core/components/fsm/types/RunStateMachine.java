package it.smartcommunitylabdhub.core.components.fsm.types;

import java.util.Map;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

import it.smartcommunitylabdhub.core.components.fsm.State;
import it.smartcommunitylabdhub.core.components.fsm.StateMachine;
import it.smartcommunitylabdhub.core.components.fsm.StateMachine.StateMachineBuilder;
import it.smartcommunitylabdhub.core.components.fsm.Transaction;
import it.smartcommunitylabdhub.core.components.fsm.enums.RunEvent;
import it.smartcommunitylabdhub.core.components.fsm.enums.RunState;
import it.smartcommunitylabdhub.core.services.interfaces.RunService;

@Component
public class RunStateMachine {

        @Autowired
        RunService runService;

        public StateMachine<RunState, RunEvent, Map<String, Object>> create(RunState initialState,
                        Map<String, Object> initialContext) {

                StateMachineBuilder<RunState, RunEvent, Map<String, Object>> builder = StateMachine
                                .<RunState, RunEvent, Map<String, Object>>builder(initialState, initialContext);

                // CREATE STATE
                State<RunState, RunEvent, Map<String, Object>> createState = new State<>();
                State<RunState, RunEvent, Map<String, Object>> readyState = new State<>();
                State<RunState, RunEvent, Map<String, Object>> runningState = new State<>();
                State<RunState, RunEvent, Map<String, Object>> completedState = new State<>();
                State<RunState, RunEvent, Map<String, Object>> errorState = new State<>();

                createState.addTransaction(
                                new Transaction<>(RunEvent.PREPARE, RunState.READY, (input, context) -> true, false));
                readyState.addTransaction(
                                new Transaction<>(RunEvent.RUNNING, RunState.RUNNING, (input, context) -> true, false));
                readyState.addTransaction(
                                new Transaction<>(RunEvent.COMPLETED, RunState.COMPLETED, (input, context) -> true,
                                                false));
                runningState.addTransaction(
                                new Transaction<>(RunEvent.COMPLETED, RunState.COMPLETED, (input, context) -> true,
                                                false));

                builder.withState(RunState.CREATED, createState)
                                .withState(RunState.READY, readyState)
                                .withState(RunState.RUNNING, runningState)
                                .withState(RunState.COMPLETED, completedState)
                                .withErrorState(RunState.ERROR, errorState)
                                .withStateChangeListener((newState, context) -> System.out.println(
                                                "State Change Listener: " + newState + ", context: " + context));

                return builder.build();
        }

}
