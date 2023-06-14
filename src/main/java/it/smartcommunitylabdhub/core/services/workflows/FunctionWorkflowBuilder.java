package it.smartcommunitylabdhub.core.services.workflows;

import java.util.AbstractMap;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Objects;
import java.util.Optional;
import java.util.function.Function;
import java.util.stream.Collectors;
import java.util.stream.Stream;

import org.springframework.core.ParameterizedTypeReference;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpMethod;
import org.springframework.http.HttpStatusCode;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Component;
import org.springframework.web.client.HttpClientErrorException;
import org.springframework.web.client.RestTemplate;

import it.smartcommunitylabdhub.core.models.accessors.enums.FunctionKind;
import it.smartcommunitylabdhub.core.models.accessors.enums.ProjectKind;
import it.smartcommunitylabdhub.core.models.accessors.kinds.interfaces.FunctionFieldAccessor;
import it.smartcommunitylabdhub.core.models.accessors.kinds.interfaces.ProjectFieldAccessor;
import it.smartcommunitylabdhub.core.models.converters.ConversionUtils;
import it.smartcommunitylabdhub.core.models.dtos.FunctionDTO;
import it.smartcommunitylabdhub.core.services.interfaces.FunctionService;
import it.smartcommunitylabdhub.core.services.workflows.factory.Workflow;
import it.smartcommunitylabdhub.core.services.workflows.factory.WorkflowFactory;

@Component
public class FunctionWorkflowBuilder {

    private static FunctionService functionService;
    private static RestTemplate restTemplate;
    private static ParameterizedTypeReference<Map<String, Object>> responseType;

    public FunctionWorkflowBuilder(FunctionService functionService) {
        FunctionWorkflowBuilder.functionService = functionService;
        FunctionWorkflowBuilder.restTemplate = new RestTemplate();
        FunctionWorkflowBuilder.responseType = new ParameterizedTypeReference<Map<String, Object>>() {
        };

    }

    public static Workflow buildWorkflow() {

        final String FUNCTION_URL = "http://192.168.49.2:30070/api/v1/func/{project}/{function}";
        final String PROJECT_URL = "http://192.168.49.2:30070/api/v1/projects/{project}";

        // COMMENT: call /{project}/{function} api and iterate over them..try to check
        @SuppressWarnings("unchecked")
        Function<String, List<FunctionDTO>> compareMlrunCoreFunctions = url -> {

            HttpHeaders headers = new HttpHeaders();
            headers.setContentType(MediaType.APPLICATION_JSON);
            HttpEntity<String> entity = new HttpEntity<>(headers);

            return functionService.getAllLatestFunctions().stream()
                    .map(function -> {
                        String requestUrl = url
                                .replace("{project}", function.getProject())
                                .replace("{function}", function.getName());

                        try {
                            ResponseEntity<Map<String, Object>> response = restTemplate
                                    .exchange(requestUrl, HttpMethod.GET, entity, responseType);

                            return Optional.ofNullable(response.getBody()).map(body -> {
                                FunctionFieldAccessor mlrunFunctionAccessor = FunctionKind
                                        .valueOf(function.getKind().toUpperCase())
                                        .createAccessor((Map<String, Object>) body.get("func"));

                                if (!mlrunFunctionAccessor.getHash()
                                        .equals(Optional.ofNullable(function.getExtra().get("mlrunHash")).orElse(""))) {
                                    // Function need to be updated in mlrun
                                    return function;
                                }
                                return null;
                            }).orElseGet(() -> null);

                        } catch (HttpClientErrorException e) {
                            HttpStatusCode statusCode = e.getStatusCode();
                            if (statusCode.is4xxClientError()) {
                                // Function will be created on mlrun
                                return function;
                            }
                            // eventually ignored
                            return null;
                        }
                    })
                    .filter(Objects::nonNull)
                    .collect(Collectors.toList());

        };

        // COMMENT: For each function on list update or create a new function in mlrun.
        @SuppressWarnings("unchecked")
        Function<List<FunctionDTO>, List<FunctionDTO>> storeFunctions = functions -> {

            HttpHeaders headers = new HttpHeaders();
            headers.setContentType(MediaType.APPLICATION_JSON);

            return functions.stream()
                    .map(function -> {
                        try {
                            String requestUrl = FUNCTION_URL
                                    .replace("{project}", function.getProject())
                                    .replace("{function}", function.getName());

                            // FIXME: check if more field are required.
                            // Convert function DTO into Map<String, Object>
                            Map<String, Object> requestBody = ConversionUtils.convert(function, "mlrunFunction");

                            // Compose request
                            HttpEntity<Map<String, Object>> entity = new HttpEntity<>(requestBody, headers);

                            // Get response
                            ResponseEntity<Map<String, Object>> response = restTemplate.exchange(requestUrl,
                                    HttpMethod.POST, entity,
                                    responseType);

                            if (response.getStatusCode().is2xxSuccessful()) {

                                // Set mlrun -> core : hash
                                Optional.ofNullable(response.getBody())
                                        .ifPresent(b -> function.setExtra("mlrunHash",
                                                (String) Optional.ofNullable(b.get("hash_key"))
                                                        .orElse("")));

                                // Set mlrun -> core : status
                                ResponseEntity<Map<String, Object>> funcResponse = restTemplate
                                        .exchange(requestUrl, HttpMethod.GET, entity, responseType);

                                Optional.ofNullable(funcResponse.getBody()).ifPresent(body -> {
                                    FunctionFieldAccessor mlrunFunctionAccessor = FunctionKind
                                            .valueOf(function.getKind().toUpperCase())
                                            .createAccessor((Map<String, Object>) body.get("func"));

                                    function.setExtra("status", mlrunFunctionAccessor.getStatus());
                                });

                                // Update our function
                                return functionService.updateFunction(function, function.getId());
                            }
                            return null;
                        } catch (HttpClientErrorException ex) {
                            return null;
                        }
                    })
                    .filter(Objects::nonNull)
                    .collect(Collectors.toList());
        };

        // COMMENT: Update project with function in mlrun
        @SuppressWarnings("unchecked")
        Function<List<FunctionDTO>, Object> updateProject = functions -> {
            HttpHeaders headers = new HttpHeaders();
            headers.setContentType(MediaType.APPLICATION_JSON);

            functions.stream().forEach(function -> {
                try {
                    String requestUrl = PROJECT_URL
                            .replace("{project}", function.getProject());

                    // Get the project
                    HttpEntity<String> entityGet = new HttpEntity<>(headers);
                    ResponseEntity<Map<String, Object>> response = restTemplate
                            .exchange(requestUrl, HttpMethod.GET, entityGet, responseType);

                    Optional.ofNullable(response.getBody()).ifPresent(body -> {
                        ProjectFieldAccessor projectFieldAccessor = ProjectKind.MLRUN.createAccessor(body);
                        FunctionFieldAccessor functionFieldAccessor = FunctionKind.valueOf(
                                function.getKind().toUpperCase())
                                .createAccessor(ConversionUtils.convert(function, "mlrunFunction"));

                        // Create a new function into project
                        Map<String, Object> newFunction = Stream.of(
                                new AbstractMap.SimpleEntry<>("name", functionFieldAccessor.getName()),
                                new AbstractMap.SimpleEntry<>("kind", functionFieldAccessor.getKind()),
                                new AbstractMap.SimpleEntry<>("image", functionFieldAccessor.getImage()),
                                new AbstractMap.SimpleEntry<>("handler", functionFieldAccessor.getDefaultHandler()))
                                .filter(entry -> entry.getValue() != null) // exclude null values
                                .collect(Collectors.toMap(Map.Entry::getKey, Map.Entry::getValue));

                        ((List<Map<String, Object>>) projectFieldAccessor
                                .getSpecs().get("functions")).add(newFunction);

                        HttpEntity<Map<String, Object>> entityPut = new HttpEntity<>(projectFieldAccessor.getFields(),
                                headers);

                        restTemplate.exchange(requestUrl,
                                HttpMethod.PUT, entityPut, responseType);

                    });

                } catch (HttpClientErrorException ex) {

                }
            });

            return null;
        };

        // Define workflow steps
        WorkflowFactory workflowFactory = WorkflowFactory.builder()
                .step(compareMlrunCoreFunctions, FUNCTION_URL)
                .step(storeFunctions)
                .step(updateProject);

        // .conditionalStep((List<FunctionFieldAccessor> s) -> s.size() > 0,
        // upsertFunction);

        Workflow workflow = workflowFactory.build();
        return workflow;
    }

}