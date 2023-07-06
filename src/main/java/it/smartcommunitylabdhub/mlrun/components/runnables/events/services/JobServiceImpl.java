package it.smartcommunitylabdhub.mlrun.components.runnables.events.services;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.core.ParameterizedTypeReference;
import org.springframework.http.*;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

import it.smartcommunitylabdhub.core.components.runnables.events.services.interfaces.KindService;
import it.smartcommunitylabdhub.core.exceptions.CoreException;
import it.smartcommunitylabdhub.core.models.accessors.utils.TaskAccessor;
import it.smartcommunitylabdhub.core.models.accessors.utils.TaskUtils;
import it.smartcommunitylabdhub.core.models.dtos.RunDTO;

import java.util.*;

@Service
public class JobServiceImpl implements KindService<Map<String, Object>> {

    @Value("${mlrun.api.submit-job}")
    private String MLRUN_API_SUBMIT_JOB;

    private final RestTemplate restTemplate;

    public JobServiceImpl() {
        this.restTemplate = new RestTemplate();
    }

    @Override
    public Map<String, Object> run(RunDTO runDTO) {
        ParameterizedTypeReference<Map<String, Object>> responseType = new ParameterizedTypeReference<>() {
        };

        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.APPLICATION_JSON);

        TaskAccessor taskAccessor = TaskUtils.parseTask(runDTO.getTask());
        Map<String, Object> requestBody = Map.of(
                "task", Map.of(
                        "spec", runDTO.getSpec(),
                        "metadata", Map.of(
                                "name",
                                taskAccessor.getProject() +
                                        "-" +
                                        taskAccessor.getName(),
                                "project", runDTO.getProject())));

        System.out.println("-----------------  REQUEST BODY ----------------");
        System.out.println(requestBody.toString());
        System.out.println("-----------------  end REQUEST BODY ----------------");
        HttpEntity<Map<String, Object>> entity = new HttpEntity<>(requestBody, headers);

        ResponseEntity<Map<String, Object>> response = restTemplate.exchange(
                MLRUN_API_SUBMIT_JOB,
                HttpMethod.POST,
                entity,
                responseType);

        if (response.getStatusCode().is2xxSuccessful()) {
            return Optional.ofNullable(response.getBody()).orElse(null);
        } else {
            String statusCode = response.getStatusCode().toString();
            String errorMessage = Optional.ofNullable(response.getBody())
                    .map(body -> body.get("detail"))
                    .map(Object::toString)
                    .orElse("");

            throw new CoreException(statusCode, errorMessage, null);
        }
    }
}
