package it.smartcommunitylabdhub.core;

import org.junit.Test;
import org.springframework.boot.test.context.SpringBootTest;

import it.smartcommunitylabdhub.core.components.fsm.StateMachine;

@SpringBootTest
public class StateMachineTest {

    // some method definition

    @Test
    public void fsm() {

        enum RegistrationState {
            START,
            PROCESSING,
            COMPLETED,
            ARCHIVED
        }

        enum RegistrationEvent {
            START_REGISTRATION,
            SUBMIT_REGISTRATION
        }

        StateMachine<RegistrationState, RegistrationEvent, String> stateMachine = new StateMachine<>(
                RegistrationState.START);

        // Add transitions
        stateMachine.addTransition(RegistrationState.START, RegistrationEvent.START_REGISTRATION,
                RegistrationState.PROCESSING, state -> true, state -> {
                    System.out.println("Executing logic for START_REGISTRATION event in state: " + state);
                    return "REGISTRATION_DATA";
                });

        stateMachine.addTransition(RegistrationState.PROCESSING, RegistrationEvent.SUBMIT_REGISTRATION,
                RegistrationState.COMPLETED, state -> true, state -> {
                    System.out.println("Executing logic for SUBMIT_REGISTRATION event in state: " + state);
                    return "SUCCESS";
                });

        // Add an auto transition
        stateMachine.addAutoTransition(RegistrationState.COMPLETED, RegistrationState.ARCHIVED,
                state -> true, state -> {
                    System.out.println("Executing logic for auto transition in state: " + state);
                    return null; // No result needed for auto transition
                });

        // Add a change listener specifically for the SUBMIT_REGISTRATION event
        stateMachine.addChangeListener(RegistrationEvent.SUBMIT_REGISTRATION, (fromState, toState, event) -> {
            System.out.println("Event change: " + fromState + " -> " + toState + " (Event: " + event + ")");
        });

        // Simulate the user registration process
        stateMachine.processEvent(RegistrationEvent.START_REGISTRATION);
        stateMachine.processEvent(RegistrationEvent.SUBMIT_REGISTRATION);

    }
}
