package it.smartcommunitylabdhub.core.components.workflows.functions;

import java.util.Map;
import java.util.Optional;
import java.util.function.Function;

import org.springframework.core.ParameterizedTypeReference;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpMethod;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Component;
import org.springframework.web.client.RestTemplate;

import it.smartcommunitylabdhub.core.components.workflows.factory.Workflow;
import it.smartcommunitylabdhub.core.components.workflows.factory.WorkflowFactory;
import it.smartcommunitylabdhub.core.exceptions.StopPoller;
import it.smartcommunitylabdhub.core.models.dtos.RunDTO;
import it.smartcommunitylabdhub.core.services.interfaces.RunService;

@Component
public class RunWorkflowBuilder extends BaseWorkflowBuilder {
    private final RunService runService;
    private final RestTemplate restTemplate;

    private static Integer i = 0;

    public RunWorkflowBuilder(RunService runService) {
        this.runService = runService;
        this.restTemplate = new RestTemplate();
    }

    public Workflow buildWorkflow(RunDTO runDTO) {
        final String RUN_URL = "http://192.168.49.2:30070/api/v1/run/{project}/{uid}";

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

                i++;

                if (i >= 5) {
                    throw new StopPoller("Poller stop");
                }

                // System.out.println("the body :" + body.toString());
                return "Stocazzo!";
            }).orElseGet(() -> null);

        };

        // Define workflow steps
        return WorkflowFactory.builder()
                .step(getRunUpdate, RUN_URL, runDTO)
                .build();
    }

}
