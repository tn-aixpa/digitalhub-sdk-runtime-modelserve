package it.smartcommunitylabdhub.core.components.runnables.services;

import java.util.HashMap;
import java.util.Map;
import java.util.Optional;

import javax.swing.text.html.Option;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.core.ParameterizedTypeReference;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpMethod;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

import it.smartcommunitylabdhub.core.components.runnables.dispatcher.MessageDispatcher;
import it.smartcommunitylabdhub.core.components.runnables.services.interfaces.JobService;
import it.smartcommunitylabdhub.core.models.builders.entities.RunEntityBuilder;
import it.smartcommunitylabdhub.core.models.dtos.RunDTO;
import it.smartcommunitylabdhub.core.models.dtos.TaskDTO;
import it.smartcommunitylabdhub.core.repositories.RunRepository;
import it.smartcommunitylabdhub.core.repositories.TaskRepository;
import jakarta.transaction.Transactional;

@Service
public class JobServiceImpl implements JobService {

    @Value("${mlrun.api.submit-job}")
    private String MLRUN_API_SUBMIT_JOB;

    private final MessageDispatcher messageDispatcher;
    private final RestTemplate restTemplate;
    private final TaskRepository taskRepository;
    private final RunRepository runRepository;

    public JobServiceImpl(MessageDispatcher messageDispatcher,
            TaskRepository taskRepository, RunRepository runRepository) {
        this.messageDispatcher = messageDispatcher;
        this.restTemplate = new RestTemplate();
        this.taskRepository = taskRepository;
        this.runRepository = runRepository;
    }

    @Override
    @Transactional
    public void run(RunDTO runDTO, TaskDTO taskDTO) {
        try {

            System.out.println("1. Call api to get run status");

            ParameterizedTypeReference<Map<String, Object>> responseType = new ParameterizedTypeReference<Map<String, Object>>() {
            };

            HttpHeaders headers = new HttpHeaders();
            headers.setContentType(MediaType.APPLICATION_JSON);

            Map<String, Object> requestBody = Map.of(
                    "task", Map.of(
                            "spec", taskDTO.getSpec(),
                            "metadata", Map.of(
                                    "name", taskDTO.getName(),
                                    "project", taskDTO.getProject())));
            HttpEntity<Map<String, Object>> entity = new HttpEntity<>(
                    requestBody, headers);

            // Get response from job submit
            ResponseEntity<Map<String, Object>> response = restTemplate
                    .exchange(MLRUN_API_SUBMIT_JOB,
                            HttpMethod.POST, entity,
                            responseType);

            if (response.getStatusCode().is2xxSuccessful()) {
                Map<String, Object> body = Optional.ofNullable(response.getBody()).orElse(new HashMap<>());

                getNestedFieldValue(body, "data").ifPresent(data -> {
                    getNestedFieldValue(data, "spec").ifPresent(spec -> {
                        runDTO.setBody(spec);
                    });

                    getNestedFieldValue(data, "metadata").ifPresent(metadata -> {
                        runDTO.setExtra("mlrun_run_uid", metadata.get("uid"));
                    });

                    getNestedFieldValue(data, "status").ifPresent(status -> {
                        runDTO.setExtra("status", status);
                    });

                    runRepository.save(new RunEntityBuilder(runDTO).build());

                    System.out.println("2. Dispatch event to event BUS");
                });

            }

        } catch (Exception e) {
            System.out.println(e.getMessage());
        }
    }

    private static Optional<Map<String, Object>> getNestedFieldValue(Map<String, Object> map, String field) {
        Object value = ((Map<?, ?>) map).get(field);

        if (value instanceof Map) {
            @SuppressWarnings("unchecked")
            Map<String, Object> nestedMap = (Map<String, Object>) value;
            return Optional.of(nestedMap);
        } else {
            return Optional.empty(); // Field path doesn't lead to a nested map
        }
    }

}
