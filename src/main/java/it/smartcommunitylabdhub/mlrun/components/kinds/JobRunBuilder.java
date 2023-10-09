package it.smartcommunitylabdhub.mlrun.components.kinds;

import java.util.Map;
import java.util.Optional;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;

import it.smartcommunitylabdhub.core.annotations.RunBuilderComponent;
import it.smartcommunitylabdhub.core.components.kinds.factory.builders.KindBuilder;
import it.smartcommunitylabdhub.core.exceptions.CoreException;
import it.smartcommunitylabdhub.core.models.accessors.utils.RunUtils;
import it.smartcommunitylabdhub.core.models.accessors.utils.TaskAccessor;
import it.smartcommunitylabdhub.core.models.accessors.utils.TaskUtils;
import it.smartcommunitylabdhub.core.models.builders.entities.FunctionEntityBuilder;
import it.smartcommunitylabdhub.core.models.entities.function.FunctionDTO;
import it.smartcommunitylabdhub.core.models.entities.run.RunDTO;
import it.smartcommunitylabdhub.core.models.entities.task.TaskDTO;
import it.smartcommunitylabdhub.core.repositories.TaskRepository;
import it.smartcommunitylabdhub.core.services.interfaces.FunctionService;
import it.smartcommunitylabdhub.core.utils.MapUtils;

@RunBuilderComponent(platform = "job", perform = "perform")
public class JobRunBuilder implements KindBuilder<TaskDTO, RunDTO> {
        @Autowired
        TaskRepository taskRepository;

        @Autowired
        FunctionService functionService;

        @Autowired
        FunctionEntityBuilder functionEntityBuilder;

        @Override
        public RunDTO build(TaskDTO taskDTO) {
                // 1. get function get if exist otherwise throw exeception.
                return taskRepository.findById(taskDTO.getId()).map(task -> {
                        // 1. produce function object for mlrun and put it on spec.
                        TaskAccessor taskAccessor = TaskUtils.parseTask(taskDTO.getFunction());

                        FunctionDTO functionDTO =
                                        functionService.getFunction(taskAccessor.getVersion());

                        // 2. set function on spec for mlrun
                        return Optional.ofNullable(functionDTO.getExtra().get("mlrun_hash"))
                                        .map(mlrunHash -> {

                                                // 3. set function on spec
                                                taskDTO.getSpec().put("function", functionDTO
                                                                .getProject() + "/"
                                                                + functionDTO.getName() + "@"
                                                                + mlrunHash);

                                                // 4. Merge Task spec with function spec
                                                // functionDTO.getSpec().putAll(taskDTO.getSpec());
                                                // MapUtils.mergeMaps(functionDTO.getSpec(),
                                                // taskDTO.getSpec());
                                                Map<String, Object> mergedSpec = MapUtils.mergeMaps(
                                                                functionDTO.getSpec(),
                                                                taskDTO.getSpec(),
                                                                (oldValue, newValue) -> newValue);


                                                // 5. produce a run object and store it
                                                return RunDTO.builder().kind("run")
                                                                .taskId(task.getId())
                                                                .project(task.getProject())
                                                                .task(RunUtils.buildRunString(
                                                                                functionDTO,
                                                                                taskDTO))
                                                                .spec(mergedSpec).build();

                                        })
                                        .orElseThrow(() -> new CoreException("MLrunHashNotFound",
                                                        "Cannot prepare mlrun function. Mlrun hash not found!",
                                                        HttpStatus.INTERNAL_SERVER_ERROR));

                }).orElseThrow(() -> new CoreException("FunctionNotFound",
                                "The function you are searching for does not exist.",
                                HttpStatus.NOT_FOUND));

        }
}
