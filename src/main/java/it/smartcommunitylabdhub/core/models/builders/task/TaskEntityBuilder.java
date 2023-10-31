package it.smartcommunitylabdhub.core.models.builders.task;

import it.smartcommunitylabdhub.core.components.infrastructure.factories.specs.SpecEntity;
import it.smartcommunitylabdhub.core.components.infrastructure.factories.specs.SpecRegistry;
import it.smartcommunitylabdhub.core.models.base.interfaces.Spec;
import it.smartcommunitylabdhub.core.models.builders.EntityFactory;
import it.smartcommunitylabdhub.core.models.converters.ConversionUtils;
import it.smartcommunitylabdhub.core.models.entities.task.Task;
import it.smartcommunitylabdhub.core.models.entities.task.TaskDTO;
import it.smartcommunitylabdhub.core.models.entities.task.specs.TaskBaseSpec;
import it.smartcommunitylabdhub.core.models.enums.State;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

@Component
public class TaskEntityBuilder {

    @Autowired
    SpecRegistry<? extends Spec> specRegistry;

    /**
     * Build a Task from a TaskDTO and store extra values as a cbor
     *
     * @param taskDTO
     * @return Task
     */
    public Task build(TaskDTO taskDTO) {
        Task task = ConversionUtils.convert(taskDTO, "task");
        // Retrieve base spec
        TaskBaseSpec taskBaseSpec = (TaskBaseSpec) specRegistry.createSpec(
                task.getKind(),
                SpecEntity.TASK,
                taskDTO.getSpec());
        // Merge function
        task.setFunction(taskBaseSpec.getFunction());
        
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
                                        taskDTO.getSpec(),
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
        TaskBaseSpec taskBaseSpec = (TaskBaseSpec) specRegistry.createSpec(
                task.getKind(),
                SpecEntity.TASK,
                taskDTO.getSpec());
        return EntityFactory.combine(
                task, taskDTO, builder -> builder
                        .with(t -> t.setFunction(taskBaseSpec.getFunction()))
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
                                ConversionUtils.convert(
                                        taskDTO.getSpec(),

                                        "cbor"))));
    }
}
