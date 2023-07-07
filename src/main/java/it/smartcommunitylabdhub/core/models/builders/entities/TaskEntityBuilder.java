package it.smartcommunitylabdhub.core.models.builders.entities;

import it.smartcommunitylabdhub.core.models.builders.EntityFactory;
import it.smartcommunitylabdhub.core.models.converters.ConversionUtils;
import it.smartcommunitylabdhub.core.models.dtos.TaskDTO;
import it.smartcommunitylabdhub.core.models.entities.Task;
import it.smartcommunitylabdhub.core.models.enums.State;

public class TaskEntityBuilder {

        private TaskDTO taskDTO;

        public TaskEntityBuilder(
                        TaskDTO taskDTO) {
                this.taskDTO = taskDTO;
        }

        /**
         * Build a Task from a TaskDTO and store extra values as a cbor
         * 
         * @return
         */
        public Task build() {
                Task Task = EntityFactory.combine(
                                ConversionUtils.convert(taskDTO, "task"), taskDTO,
                                builder -> {
                                        builder
                                                        .with(f -> f.setExtra(
                                                                        ConversionUtils.convert(taskDTO.getExtra(),
                                                                                        "cbor")))
                                                        .with(f -> f.setSpec(
                                                                        ConversionUtils.convert(taskDTO.getSpec(),
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
                                Task, taskDTO, builder -> {
                                        builder
                                                        .with(f -> f.setTask(taskDTO.getTask()))
                                                        .with(f -> f.setKind(taskDTO.getKind()))
                                                        .with(f -> f.setProject(taskDTO.getProject()))
                                                        .with(f -> f.setState(taskDTO.getState() == null
                                                                        ? State.CREATED
                                                                        : State.valueOf(taskDTO.getState())))
                                                        .with(f -> f.setExtra(
                                                                        ConversionUtils.convert(taskDTO.getExtra(),

                                                                                        "cbor")))
                                                        .with(f -> f.setSpec(
                                                                        ConversionUtils.convert(taskDTO.getSpec(),

                                                                                        "cbor")));
                                });
        }
}