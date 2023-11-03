package it.smartcommunitylabdhub.core.models.builders.task;

import it.smartcommunitylabdhub.core.models.builders.EntityFactory;
import it.smartcommunitylabdhub.core.models.converters.ConversionUtils;
import it.smartcommunitylabdhub.core.models.entities.task.Task;
import it.smartcommunitylabdhub.core.models.entities.task.TaskDTO;
import it.smartcommunitylabdhub.core.models.entities.task.specs.TaskBaseSpec;
import it.smartcommunitylabdhub.core.models.enums.State;
import it.smartcommunitylabdhub.core.utils.JacksonMapper;
import org.springframework.stereotype.Component;

@Component
public class TaskEntityBuilder {

    /**
     * Build a Task from a TaskDTO and store extra values as a cbor
     *
     * @param taskDTO
     * @return Task
     */
    public Task build(TaskDTO taskDTO) {
        // Retrieve the task
        Task task = ConversionUtils.convert(taskDTO, "task");

        // Retrieve base spec
        TaskBaseSpec spec = JacksonMapper.objectMapper
                .convertValue(taskDTO.getSpec(), TaskBaseSpec.class);

        // Merge function
        task.setFunction(spec.getFunction());

        return EntityFactory.combine(
                task, taskDTO,
                builder -> builder
                        .with(t -> t.setMetadata(
                                ConversionUtils.convert(taskDTO
                                                .getMetadata(),
                                        "metadata")))

                        .with(t -> t.setExtra(
                                ConversionUtils.convert(
                                        taskDTO.getExtra(),
                                        "cbor")))
                        .with(t -> t.setSpec(
                                ConversionUtils.convert(
                                        spec.toMap(),
                                        "cbor"))));
    }

    /**
     * Update a Task if element is not passed it override causing empty field
     *
     * @param task
     * @param taskDTO
     * @return
     */
    public Task update(Task task, TaskDTO taskDTO) {
        // Retrieve base spec
        TaskBaseSpec spec = JacksonMapper.objectMapper
                .convertValue(taskDTO.getSpec(), TaskBaseSpec.class);

        return EntityFactory.combine(
                task, taskDTO, builder -> builder
                        .with(t -> t.setFunction(spec.getFunction()))
                        .with(t -> t.setKind(taskDTO.getKind()))
                        .with(t -> t.setProject(taskDTO.getProject()))
                        .with(t -> t.setState(taskDTO.getState() == null
                                ? State.CREATED
                                : State.valueOf(taskDTO
                                .getState())))
                        .with(t -> t.setMetadata(
                                ConversionUtils.convert(taskDTO
                                                .getMetadata(),
                                        "metadata")))

                        .with(t -> t.setExtra(
                                ConversionUtils.convert(
                                        taskDTO.getExtra(),

                                        "cbor")))
                        .with(t -> t.setSpec(
                                ConversionUtils.convert(spec.toMap(),
                                        "cbor"))));
    }
}
