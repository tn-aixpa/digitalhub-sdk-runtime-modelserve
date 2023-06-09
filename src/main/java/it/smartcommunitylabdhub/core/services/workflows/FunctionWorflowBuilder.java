package it.smartcommunitylabdhub.core.services.workflows;

import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.function.Function;
import java.util.stream.Collectors;

import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.stereotype.Component;
import org.springframework.web.client.RestTemplate;

import it.smartcommunitylabdhub.core.models.accessors.enums.FunctionKind;
import it.smartcommunitylabdhub.core.models.accessors.kinds.interfaces.FunctionFieldAccessor;
import it.smartcommunitylabdhub.core.models.dtos.FunctionDTO;
import it.smartcommunitylabdhub.core.repositories.ProjectRepository;
import it.smartcommunitylabdhub.core.services.interfaces.FunctionService;
import it.smartcommunitylabdhub.core.services.workflows.factory.Workflow;
import it.smartcommunitylabdhub.core.services.workflows.factory.WorkflowFactory;

@Component
public class FunctionWorflowBuilder {

    private static FunctionService functionService;
    private static ProjectRepository projectRepository;

    public FunctionWorflowBuilder(ProjectRepository projectRepository,
            FunctionService functionService) {
        FunctionWorflowBuilder.projectRepository = projectRepository;
        FunctionWorflowBuilder.functionService = functionService;
    }

    public static Workflow buildWorkflow() {

        // COMMENT: get all projects
        @SuppressWarnings("unchecked")
        Function<String, Map<String, List<Map<String, Object>>>> getProjects = url -> {

            // FIXME:: start from our projects not from mlrun projects
            RestTemplate restTemplate = new RestTemplate();
            HttpHeaders headers = new HttpHeaders();
            headers.setContentType(MediaType.APPLICATION_JSON);
            return restTemplate.getForObject(url, Map.class);
        };

        // COMMENT: Iterate over projects and get all functions for each projects
        Function<Map<String, List<Map<String, Object>>>, Object> getFunctions = projects -> {
            String functionPath = "http://192.168.49.2:30070/api/v1/funcs?";
            RestTemplate restTemplate = new RestTemplate();
            HttpHeaders headers = new HttpHeaders();
            headers.setContentType(MediaType.APPLICATION_JSON);

            return projects.get("project_summaries")
                    .stream()
                    .map(project -> {
                        return restTemplate.getForObject(
                                functionPath + project.get("name"),
                                Map.class);

                    })
                    .collect(Collectors.toList());
        };

        // COMMENT: Convert functions to Function specific accessor -> flat functions
        Function<List<Map<String, List<Map<String, Object>>>>, List<FunctionFieldAccessor>> toFunctionAccessor = functions -> {
            List<FunctionFieldAccessor> accessors = functions
                    .stream()
                    .map(projectFunctions -> {
                        return projectFunctions.get("funcs")
                                .stream()
                                .map(func -> {
                                    FunctionFieldAccessor functionAccessor = FunctionKind
                                            .valueOf(func.get("kind").toString().toUpperCase()).createAccessor(func);

                                    return functionAccessor;
                                })
                                .collect(Collectors.toList());
                    }).collect(Collectors.toList()).stream().flatMap(List::stream).collect(Collectors.toList());

            return accessors;
        };

        // COMMENT: Upsert Function - Mlrun <-> Core sync
        // 1. Iterate over function field accessor
        // 2. Check if project exist
        // 3. Check if function exist, if "yes" update function if "no" create function
        // 4. If my function is recent then the one that mlrun old, update the Mlrun
        // function via API

        Function<List<FunctionFieldAccessor>, Object> upsertFunction = functionAccessors -> {

            functionAccessors.stream().forEach(functionAccessor -> {
                if (projectRepository.existsByName(functionAccessor.getProject())) {
                    // check function exist!
                    Optional.ofNullable(functionService.getFunction(null))
                            .map(func -> {
                                // Check date to see if function I'm getting is newer
                                if (func.getUpdated().compareTo(functionAccessor.getUpdate()) < 0) {
                                    // replace create a new dto from accessor
                                    return FunctionDTO.builder()
                                            .kind(functionAccessor.getKind())
                                            .name(functionAccessor.getName())
                                            .project(functionAccessor.getProject())
                                            .spec(functionAccessor.getSpecs())
                                            .build();
                                } else {
                                    // Update Mlrun function with mine. { Check mlrun documentation }
                                }
                                return func;
                            }).orElseGet(() -> {
                                FunctionDTO functionDTO = FunctionDTO.builder()
                                        .kind(functionAccessor.getKind())
                                        .name(functionAccessor.getName())
                                        .project(functionAccessor.getProject())
                                        .spec(functionAccessor.getSpecs())
                                        .build();
                                functionDTO.setExtra("uuid", functionAccessor.getHash());
                                // add all other fields

                                return functionDTO;
                            });

                }
            });
            return functionAccessors;
        };

        // Define workflow steps
        WorkflowFactory workflowFactory = WorkflowFactory.builder()
                .step(getProjects, "http://192.168.49.2:30070/api/v1/project-summaries")
                .step(getFunctions)
                .step(toFunctionAccessor)
                .step(upsertFunction);
        // .conditionalStep((List<FunctionFieldAccessor> s) -> s.size() > 0,
        // upsertFunction);

        Workflow workflow = workflowFactory.build();
        return workflow;
    }

}