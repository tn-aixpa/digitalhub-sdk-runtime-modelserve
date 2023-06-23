package it.smartcommunitylabdhub.core;

import java.util.HashMap;
import java.util.Map;
import java.util.Optional;
import java.util.function.Predicate;

import org.junit.Test;
import org.springframework.boot.test.context.SpringBootTest;

import it.smartcommunitylabdhub.core.components.fsm.*;

@SpringBootTest
public class StateMachineTest {

    // some method definition

    @Test
    public void fsm() {

        // Create the state machine
        StateMachine<String, String, Map<String, Object>> stateMachine = new StateMachine<>("State1",
                new HashMap<>());

        // Create states
        State<String, String, Map<String, Object>> state1 = new State<>();
        State<String, String, Map<String, Object>> state2 = new State<>();
        State<String, String, Map<String, Object>> state3 = new State<>();
        State<String, String, Map<String, Object>> state4 = new State<>();
        State<String, String, Map<String, Object>> errorState = new State<>(); // Error state

        // Add states to the state machine
        stateMachine.addState("State1", state1);
        stateMachine.addState("State2", state2);
        stateMachine.addState("State3", state3);
        stateMachine.addState("State4", state4);

        // Define transactions for state 1
        state1.addTransaction(new Transaction<>("Event1", "State2",
                (input, context) -> input.isPresent(), false));

        // Define transactions for state 2
        state2.addTransaction(new Transaction<>("Event2", "State3",
                (input, context) -> input.isPresent(), false));

        // Define transactions for state 3
        state3.addTransaction(new Transaction<>("Event3", "State4",
                (input, context) -> input.isPresent(), false));

        // Define transactions for state 4
        state4.addTransaction(new Transaction<>("Event4", "State1",
                (input, context) -> input.isPresent(), false));

        // Set internal logic for state 2
        state1.setInternalLogic((String input, Map<String, Object> context) -> {
            System.out.println("Executing internal logic of State1 with input: " + input + ", context: " + context);
            context.put("value", 1);
            return Optional.of("State1 Result");
        });
        state1.setExitAction((Map<String, Object> context) -> {
            System.out.println("exit action for state 1");
        });

        state2.setInternalLogic((String input, Map<String, Object> context) -> {
            System.out.println("Executing internal logic of State2 with input: " + input + ", context: " + context);
            context.put("value", 2);
            return Optional.of("State2 Result");
        });

        // Set internal logic for state 3
        state3.setInternalLogic((String input, Map<String, Object> context) -> {
            System.out.println("Executing internal logic of State3 with input: " + input + ", context: " + context);
            context.put("value", 3);
            return Optional.of("State3 Result");
        });

        // Set internal logic for state 4
        state4.setInternalLogic((String input, Map<String, Object> context) -> {
            System.out.println("Executing internal logic of State4 with input: " + input + ", context: " + context);
            context.put("value", 4);
            return Optional.of("State4 Result");
        });

        // Set internal logic for the error state
        errorState.setInternalLogic((String input, Map<String, Object> context) -> {
            System.out.println("Error state reached. Input: " + input + ", context: " + context);
            // Handle error logic here
            return Optional.empty(); // No result for error state
        });

        // Add event listeners
        stateMachine.addEventListener("Event1",
                (String input, Map<String, Object> context) -> System.out
                        .println("Event1 Listener: " + input + ", context: " + context));
        stateMachine.addEventListener("Event2",
                (String input, Map<String, Object> context) -> System.out
                        .println("Event2 Listener: " + input + ", context: " + context));
        stateMachine.addEventListener("Event3",
                (String input, Map<String, Object> context) -> System.out
                        .println("Event3 Listener: " + input + ", context: " + context));
        stateMachine.addEventListener("Event4",
                (String input, Map<String, Object> context) -> System.out
                        .println("Event4 Listener: " + input + ", context: " + context));

        // Set state change listener
        stateMachine.setStateChangeListener((String newState, Map<String, Object> context) -> System.out
                .println("State Change Listener: " + newState + ", context: " + context));

        // Set the error state
        stateMachine.setErrorState("ErrorState", errorState);

        // Trigger events to test the state machine
        stateMachine.processEvent("Event1", Optional.of("Input1"));
        stateMachine.processEvent("Event4", Optional.of("Input2"));

    }
}
