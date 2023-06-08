package it.smartcommunitylabdhub.core.services.workflows;

import java.io.IOException;
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.util.List;
import java.util.Map;
import java.util.function.Function;

import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;

import it.smartcommunitylabdhub.core.services.workflows.factory.Workflow;
import it.smartcommunitylabdhub.core.services.workflows.factory.WorkflowFactory;

public class FunctionWorflowBuilder {

    public static Workflow buildWorkflow() {

        // Get all functions
        Function<Object, Object> getRequest = url -> {
            HttpClient httpClient = HttpClient.newHttpClient();
            HttpRequest request = HttpRequest.newBuilder()
                    .uri(URI.create((String) url))
                    .build();
            try {
                HttpResponse<String> response = httpClient.send(request, HttpResponse.BodyHandlers.ofString());
                String responseBody = response.body();

                // Parse JSON response into a Map<String, Object>
                ObjectMapper objectMapper = new ObjectMapper();
                List<Map<String, Object>> responseMap = objectMapper.readValue(responseBody,
                        new TypeReference<List<Map<String, Object>>>() {
                        });

                return responseMap;
            } catch (IOException | InterruptedException e) {
                throw new RuntimeException();
            }
        };
        WorkflowFactory workflowFactory = WorkflowFactory.builder()
                .step(getRequest, "http://192.168.49.2:30070/api/v1/project-summaries");

        Workflow workflow = workflowFactory.build();

        return workflow;
    }

}
