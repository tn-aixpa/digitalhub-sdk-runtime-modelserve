package it.smartcommunitylabdhub.core.models.builders.task;

import it.smartcommunitylabdhub.core.components.infrastructure.factories.specs.SpecRegistry;
import it.smartcommunitylabdhub.core.models.base.interfaces.Spec;
import it.smartcommunitylabdhub.core.models.builders.EntityFactory;
import it.smartcommunitylabdhub.core.models.converters.ConversionUtils;
import it.smartcommunitylabdhub.core.models.converters.types.MetadataConverter;
import it.smartcommunitylabdhub.core.models.entities.task.Task;
import it.smartcommunitylabdhub.core.models.entities.task.TaskDTO;
import it.smartcommunitylabdhub.core.models.entities.task.metadata.TaskMetadata;
import it.smartcommunitylabdhub.core.models.enums.State;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

import java.util.Map;
import java.util.Optional;


@Component
public class TaskDTOBuilder {

    @Autowired
    SpecRegistry<? extends Spec> specRegistry;

    @Autowired
    MetadataConverter<TaskMetadata> metadataConverter;

    /**
     * Build a taskDTO given a task
     *
     * @param task
     * @return TaskDTO
     */
    public TaskDTO build(Task task) {

        // Retrieve spec
        Map<String, Object> spec = ConversionUtils.reverse(task.getSpec(), "cbor");

        // Find base task spec
        Spec taskSpec = specRegistry.createSpec(task.getKind(), spec);

        // Add base spec to the one stored in db
        spec.putAll(taskSpec.toMap());

        return EntityFactory.create(TaskDTO::new, task, builder -> builder
                .with(dto -> dto.setId(task.getId()))
                .with(dto -> dto.setProject(task.getProject()))
                .with(dto -> dto.setKind(task.getKind()))
                .with(dto -> dto.setMetadata(Optional
                        .ofNullable(metadataConverter.reverseByClass(
                                task.getMetadata(),
                                TaskMetadata.class))
                        .orElseGet(TaskMetadata::new)

                ))
                .with(dto -> dto.setSpec(spec))
                .with(dto -> dto.setExtra(
                        ConversionUtils.reverse(
                                task.getExtra(),
                                "cbor")))
                .with(dto -> dto.setCreated(task.getCreated()))
                .with(dto -> dto.setUpdated(task.getUpdated()))
                .with(dto -> dto.setState(task.getState() == null
                        ? State.CREATED.name()
                        : task.getState()
                        .name()))

        );
    }
}
