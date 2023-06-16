package it.smartcommunitylabdhub.core.components.runnables.services;

import java.util.Map;

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
import it.smartcommunitylabdhub.core.models.dtos.RunDTO;
import it.smartcommunitylabdhub.core.models.dtos.TaskDTO;
import it.smartcommunitylabdhub.core.models.entities.Task;
import it.smartcommunitylabdhub.core.repositories.TaskRepository;
import jakarta.transaction.Transactional;
import kotlin.sequences.TakeSequence;

@Service
public class JobServiceImpl implements JobService {

    @Value("${mlrun.api.submit-job}")
    private String MLRUN_API_SUBMIT_JOB;

    private final MessageDispatcher messageDispatcher;
    private final RestTemplate restTemplate;
    private final TaskRepository taskRepository;

    public JobServiceImpl(MessageDispatcher messageDispatcher, TaskRepository taskRepository) {
        this.messageDispatcher = messageDispatcher;
        this.restTemplate = new RestTemplate();
        this.taskRepository = taskRepository;
    }

    @Override
    @Transactional
    public void run(RunDTO runDTO, TaskDTO taskDTO) {
        // TODO Auto-generated method stub
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
            System.out.println(response.getBody().toString());
        }
        System.out.println("2. Dispatch event to event BUS");

    }

}
