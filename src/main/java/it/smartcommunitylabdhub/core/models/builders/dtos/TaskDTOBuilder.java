package it.smartcommunitylabdhub.core.models.builders.dtos;

import it.smartcommunitylabdhub.core.models.builders.EntityFactory;
import it.smartcommunitylabdhub.core.models.converters.ConversionUtils;
import it.smartcommunitylabdhub.core.models.dtos.TaskDTO;
import it.smartcommunitylabdhub.core.models.entities.Task;
import it.smartcommunitylabdhub.core.models.enums.State;

public class TaskDTOBuilder {

        private Task task;

        public TaskDTOBuilder(
                        Task task) {
                this.task = task;
        }

        public TaskDTO build() {
                return EntityFactory.create(TaskDTO::new, task, builder -> {
                        builder
                                        .with(dto -> dto.setId(task.getId()))
                                        .with(dto -> dto.setTask(task.getKind()))
                                        .with(dto -> dto.setProject(task.getProject()))
                                        .with(dto -> dto.setTask(task.getTask()))
                                        .with(dto -> dto.setSpec(ConversionUtils.reverse(task.getSpec(), "cbor")))
                                        .with(dto -> dto.setExtra(ConversionUtils.reverse(task.getExtra(), "cbor")))
                                        .with(dto -> dto.setCreated(task.getCreated()))
                                        .with(dto -> dto.setUpdated(task.getUpdated()))
                                        .with(dto -> dto.setState(task.getState() == null
                                                        ? State.CREATED.name()
                                                        : task.getState()
                                                                        .name()));

                });
        }
}