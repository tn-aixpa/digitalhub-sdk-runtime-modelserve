package it.smartcommunitylabdhub.mlrun.components.pollers.functions;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.function.Function;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpMethod;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.client.RestTemplate;

import com.fasterxml.jackson.databind.ObjectMapper;

import it.smartcommunitylabdhub.core.annotations.RunWorkflowComponent;
import it.smartcommunitylabdhub.core.components.fsm.StateMachine;
import it.smartcommunitylabdhub.core.components.fsm.enums.RunEvent;
import it.smartcommunitylabdhub.core.components.fsm.enums.RunState;
import it.smartcommunitylabdhub.core.components.fsm.types.RunStateMachine;
import it.smartcommunitylabdhub.core.components.kinds.factory.workflows.KindWorkflow;
import it.smartcommunitylabdhub.core.components.runnables.pollers.workflows.factory.Workflow;
import it.smartcommunitylabdhub.core.components.runnables.pollers.workflows.factory.WorkflowFactory;
import it.smartcommunitylabdhub.core.components.runnables.pollers.workflows.functions.BaseWorkflowBuilder;
import it.smartcommunitylabdhub.core.exceptions.StopPoller;
import it.smartcommunitylabdhub.core.models.accessors.enums.DataItemKind;
import it.smartcommunitylabdhub.core.models.accessors.kinds.interfaces.DataItemFieldAccessor;
import it.smartcommunitylabdhub.core.models.dtos.ArtifactDTO;
import it.smartcommunitylabdhub.core.models.dtos.LogDTO;
import it.smartcommunitylabdhub.core.models.dtos.RunDTO;
import it.smartcommunitylabdhub.core.services.interfaces.ArtifactService;
import it.smartcommunitylabdhub.core.services.interfaces.LogService;
import it.smartcommunitylabdhub.core.services.interfaces.RunService;
import it.smartcommunitylabdhub.core.utils.MapUtils;

@RunWorkflowComponent(type = "job")
public class JobWorkflowBuilder extends BaseWorkflowBuilder implements KindWorkflow<RunDTO, Workflow> {

    @Value("${mlrun.api.run-url}")
    private String runUrl;

    @Value("${mlrun.api.log-url}")
    private String logUrl;

    private final RunService runService;
    private final LogService logService;
    private final ArtifactService artifactService;
    private final RunStateMachine runStateMachine;
    private final RestTemplate restTemplate;
    private StateMachine<RunState, RunEvent, Map<String, Object>> stateMachine;

    ObjectMapper objectMapper = new ObjectMapper();

    public JobWorkflowBuilder(
            RunService runService,
            LogService logService,
            ArtifactService artifactService,
            RunStateMachine runStateMachine) {
        this.runService = runService;
        this.logService = logService;
        this.artifactService = artifactService;
        this.restTemplate = new RestTemplate();
        this.runStateMachine = runStateMachine;
    }

    @SuppressWarnings("unchecked")
    public Workflow build(RunDTO runDTO) {

        Function<Object[], Object> getRunUpdate = params -> {

            try {
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

                // FIXME: delete log below
                try {
                    System.out.println(objectMapper.writeValueAsString(response));
                } catch (Exception e) {
                }

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

                        // Update run state
                        runDTO.setState(stateMachine.getCurrentState().name());

                        // Store change
                        this.runService.save(runDTO);

                    } else if (stateMachine.getCurrentState().equals(RunState.COMPLETED)) {
                        // Get response body and store log as well as artifacts if present.
                        Optional.ofNullable(response.getBody()).ifPresentOrElse(b -> {
                            // Get run uid from mlrun.
                            MapUtils.getNestedFieldValue(b, "data").ifPresent(data -> {
                                MapUtils.getNestedFieldValue(data, "metadata").ifPresent(metadata -> {
                                    String uid = (String) metadata.get("uid");

                                    // Call mlrun api to get log of specific run uid.
                                    ResponseEntity<String> logResponse = restTemplate
                                            .exchange(
                                                    logUrl.replace("{project}", runDTO.getProject()).replace("{uid}",
                                                            uid),
                                                    HttpMethod.GET, entity,
                                                    String.class);

                                    // Create and store log
                                    System.out.println(logResponse.getBody());

                                    logService.createLog(LogDTO.builder()
                                            .body(Map.of("content", logResponse.getBody()))
                                            .project(runDTO.getProject())
                                            .run(runDTO.getId()).build());
                                });

                                // get Artifacts from results
                                MapUtils.getNestedFieldValue(data, "status").ifPresent(metadata -> {
                                    ((List<Map<String, Object>>) metadata.get("artifacts")).stream()
                                            .forEach(artifact -> {
                                                DataItemFieldAccessor mlrunDataItemAccessor = DataItemKind
                                                        .valueOf(artifact.get("kind").toString().toUpperCase())
                                                        .createAccessor(artifact);

                                                // Create artifact
                                                ArtifactDTO artifactDTO = ArtifactDTO.builder()
                                                        .name(mlrunDataItemAccessor.getTree())
                                                        .project(mlrunDataItemAccessor.getProject())
                                                        .kind(mlrunDataItemAccessor.getKind())
                                                        .spec(mlrunDataItemAccessor.getSpecs())
                                                        .state(mlrunDataItemAccessor.getState().toUpperCase())
                                                        .build();

                                                // Store artifact
                                                this.artifactService.createArtifact(artifactDTO);

                                            });
                                });
                            });
                        }, () -> {
                            // Could not receive body from mlrun..stop poller now
                            throw new StopPoller(
                                    "Poller complete with ERROR {Mlrun body not found}");
                        });

                        // Poller complete successfully
                        throw new StopPoller("Poller complete SUCCESSFULLY");

                    } else if (stateMachine.getCurrentState().equals(RunState.ERROR)) {

                        // State machine goes Error, stop poller
                        throw new StopPoller("Poller complete with ERROR");
                    }
                    return null;
                }).orElseGet(() -> null);

            } catch (Exception e) {
                System.out.println(e.getMessage() + " -> Stop Poller now!");
                throw new StopPoller("STOP");
            }

        };

        // Init run state machine considering current state and context.
        stateMachine = runStateMachine.create(RunState.valueOf(runDTO.getState()), new HashMap<>());
        // (Map<String, Object>) runDTO.getExtra().get("context"));

        stateMachine.processEvent(RunEvent.BUILD, Optional.empty());

        // Define workflow steps
        return WorkflowFactory.builder().step(getRunUpdate, runUrl, runDTO).build();
    }

}
