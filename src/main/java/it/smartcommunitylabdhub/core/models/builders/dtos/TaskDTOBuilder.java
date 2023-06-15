package it.smartcommunitylabdhub.core.models.builders.dtos;

import it.smartcommunitylabdhub.core.models.builders.EntityFactory;
import it.smartcommunitylabdhub.core.models.converters.ConversionUtils;
import it.smartcommunitylabdhub.core.models.dtos.TaskDTO;
import it.smartcommunitylabdhub.core.models.entities.Task;
import it.smartcommunitylabdhub.core.models.enums.State;

public class TaskDTOBuilder {

        private Task Task;

        public TaskDTOBuilder(
                        Task Task) {
                this.Task = Task;
        }

        public TaskDTO build() {
                return EntityFactory.create(TaskDTO::new, Task, builder -> {
                        builder
                                        .with(dto -> dto.setId(Task.getId()))
                                        .with(dto -> dto.setType(Task.getType()))
                                        .with(dto -> dto.setProject(Task.getProject()))
                                        .with(dto -> dto.setName(Task.getName()))
                                        .with(dto -> dto.setSpec(ConversionUtils.reverse(Task.getSpec(), "cbor")))
                                        .with(dto -> dto.setExtra(ConversionUtils.reverse(Task.getExtra(), "cbor")))
                                        .with(dto -> dto.setCreated(Task.getCreated()))
                                        .with(dto -> dto.setUpdated(Task.getUpdated()))
                                        .with(dto -> dto.setState(Task.getState() == null
                                                        ? State.CREATED.name()
                                                        : Task.getState()
                                                                        .name()));

                });
        }
}