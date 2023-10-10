package it.smartcommunitylabdhub.core.models.builders.dtos;

import java.util.Optional;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

import it.smartcommunitylabdhub.core.models.builders.EntityFactory;
import it.smartcommunitylabdhub.core.models.converters.ConversionUtils;
import it.smartcommunitylabdhub.core.models.converters.types.MetadataConverter;
import it.smartcommunitylabdhub.core.models.entities.task.Task;
import it.smartcommunitylabdhub.core.models.entities.task.TaskDTO;
import it.smartcommunitylabdhub.core.models.entities.task.TaskMetadata;
import it.smartcommunitylabdhub.core.models.enums.State;

@Component
public class TaskDTOBuilder {

        @Autowired
        MetadataConverter<TaskMetadata> metadataConverter;

        public TaskDTO build(Task task) {
                return EntityFactory.create(TaskDTO::new, task, builder -> builder
                                .with(dto -> dto.setId(task.getId()))
                                .with(dto -> dto.setFunction(task.getFunction()))
                                .with(dto -> dto.setProject(task.getProject()))
                                .with(dto -> dto.setKind(task.getKind()))
                                .with(dto -> dto.setMetadata(Optional
                                                .ofNullable(metadataConverter.reverseByClass(
                                                                task.getMetadata(),
                                                                TaskMetadata.class))
                                                .orElseGet(TaskMetadata::new)

                                ))
                                .with(dto -> dto.setSpec(
                                                ConversionUtils.reverse(task.getSpec(), "cbor")))
                                .with(dto -> dto.setExtra(
                                                ConversionUtils.reverse(task.getExtra(), "cbor")))
                                .with(dto -> dto.setCreated(task.getCreated()))
                                .with(dto -> dto.setUpdated(task.getUpdated()))
                                .with(dto -> dto.setState(task.getState() == null
                                                ? State.CREATED.name()
                                                : task.getState()
                                                                .name()))

                );
        }
}
