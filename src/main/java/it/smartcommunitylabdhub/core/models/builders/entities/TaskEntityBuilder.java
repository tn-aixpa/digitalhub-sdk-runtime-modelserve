package it.smartcommunitylabdhub.core.models.builders.entities;

import it.smartcommunitylabdhub.core.models.builders.EntityFactory;
import it.smartcommunitylabdhub.core.models.converters.ConversionUtils;
import it.smartcommunitylabdhub.core.models.dtos.TaskDTO;
import it.smartcommunitylabdhub.core.models.entities.Task;
import it.smartcommunitylabdhub.core.models.enums.State;

public class TaskEntityBuilder {

        private TaskDTO TaskDTO;

        public TaskEntityBuilder(
                        TaskDTO TaskDTO) {
                this.TaskDTO = TaskDTO;
        }

        /**
         * Build a Task from a TaskDTO and store extra values as a cbor
         * 
         * @return
         */
        public Task build() {
                Task Task = EntityFactory.combine(
                                ConversionUtils.convert(TaskDTO, "task"), TaskDTO,
                                builder -> {
                                        builder
                                                        .with(f -> f.setExtra(
                                                                        ConversionUtils.convert(TaskDTO.getExtra(),
                                                                                        "cbor")))
                                                        .with(f -> f.setSpec(
                                                                        ConversionUtils.convert(TaskDTO.getSpec(),
                                                                                        "cbor")));
                                });

                return Task;
        }

        /**
         * Update a Task
         * TODO: x because if element is not passed it override causing empty field
         * 
         * @param Task
         * @return
         */
        public Task update(Task Task) {
                return EntityFactory.combine(
                                Task, TaskDTO, builder -> {
                                        builder
                                                        .with(f -> f.setType(TaskDTO.getType()))
                                                        .with(f -> f.setProject(TaskDTO.getProject()))
                                                        .with(f -> f.setState(TaskDTO.getState() == null
                                                                        ? State.CREATED
                                                                        : State.valueOf(TaskDTO.getState())))
                                                        .with(f -> f.setExtra(
                                                                        ConversionUtils.convert(TaskDTO.getExtra(),

                                                                                        "cbor")))
                                                        .with(f -> f.setSpec(
                                                                        ConversionUtils.convert(TaskDTO.getSpec(),

                                                                                        "cbor")));
                                });
        }
}