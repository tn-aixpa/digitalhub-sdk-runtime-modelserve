package it.smartcommunitylabdhub.core.components.runnables.pollers.workflows.functions;

import java.util.HashMap;
import java.util.Map;
import java.util.Optional;
import java.util.function.Function;

import javax.swing.text.html.Option;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpMethod;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Component;
import org.springframework.web.client.RestTemplate;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;

import it.smartcommunitylabdhub.core.components.fsm.StateMachine;
import it.smartcommunitylabdhub.core.components.fsm.enums.RunEvent;
import it.smartcommunitylabdhub.core.components.fsm.enums.RunState;
import it.smartcommunitylabdhub.core.components.fsm.types.RunStateMachine;
import it.smartcommunitylabdhub.core.components.runnables.pollers.workflows.factory.Workflow;
import it.smartcommunitylabdhub.core.components.runnables.pollers.workflows.factory.WorkflowFactory;
import it.smartcommunitylabdhub.core.exceptions.StopPoller;
import it.smartcommunitylabdhub.core.models.dtos.RunDTO;
import it.smartcommunitylabdhub.core.services.interfaces.RunService;

@Component
public class RunWorkflowBuilder extends BaseWorkflowBuilder {

    @Value("${mlrun.api.run-url}")
    private String runUrl;

    private final RunService runService;
    private final RunStateMachine runStateMachine;
    private final RestTemplate restTemplate;
    private StateMachine<RunState, RunEvent, Map<String, Object>> stateMachine;

    ObjectMapper objectMapper = new ObjectMapper();

    public RunWorkflowBuilder(RunService runService, RunStateMachine runStateMachine) {
        this.runService = runService;
        this.restTemplate = new RestTemplate();
        this.runStateMachine = runStateMachine;
    }

    @SuppressWarnings("unchecked")
    public Workflow buildWorkflow(RunDTO runDTO) {
        Function<Object[], Object> getRunUpdate = params -> {

            HttpHeaders headers = new HttpHeaders();
            headers.setContentType(MediaType.APPLICATION_JSON);
            HttpEntity<String> entity = new HttpEntity<>(headers);

            String requestUrl = params[0].toString()
                    .replace("{project}", ((RunDTO) params[1]).getProject())
                    .replace("{uid}", ((RunDTO) params[1]).getExtra()
                            .get("mlrun_run_uid").toString());

            ResponseEntity<Map<String, Object>> response = restTemplate
                    .exchange(requestUrl, HttpMethod.GET, entity,
                            responseType);

            return Optional.ofNullable(response.getBody()).map(body -> {
                Map<String, Object> status = (Map<String, Object>) ((Map<String, Object>) body.get("data"))
                        .get("status");

                if (!stateMachine.getCurrentState()
                        .equals(RunState.valueOf(status.get("state").toString().toUpperCase()))) {

                    String mlrunState = status.get("state").toString();
                    stateMachine.processEvent(
                            Optional.ofNullable(RunEvent.valueOf(mlrunState.toUpperCase()))
                                    .orElseGet(() -> RunEvent.ERROR),
                            Optional.empty());

                } else if (stateMachine.getCurrentState().equals(RunState.COMPLETED)) {
                    System.out.println("Poller complete SUCCESSFULLY. Get log and stop poller now");

                    throw new StopPoller("Poller complete successful!");
                }
                return null;
            }).orElseGet(() -> null);

        };

        // Init run state machine considering current state and context.
        stateMachine = runStateMachine.create(RunState.valueOf(runDTO.getState()), new HashMap<>());
        // (Map<String, Object>) runDTO.getExtra().get("context"));

        stateMachine.processEvent(RunEvent.PREPARE, Optional.empty());

        // Define workflow steps
        return WorkflowFactory.builder().step(getRunUpdate, runUrl, runDTO).build();
    }

}
