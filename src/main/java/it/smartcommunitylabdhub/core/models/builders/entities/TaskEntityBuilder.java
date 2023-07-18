package it.smartcommunitylabdhub.core.models.builders.entities;

import org.springframework.stereotype.Component;

import it.smartcommunitylabdhub.core.models.builders.EntityFactory;
import it.smartcommunitylabdhub.core.models.converters.ConversionUtils;
import it.smartcommunitylabdhub.core.models.dtos.TaskDTO;
import it.smartcommunitylabdhub.core.models.entities.Task;
import it.smartcommunitylabdhub.core.models.enums.State;

@Component
public class TaskEntityBuilder {

        /**
         * Build a Task from a TaskDTO and store extra values as a cbor
         * 
         * @return
         */
        public Task build(TaskDTO taskDTO) {
                return EntityFactory.combine(
                                ConversionUtils.convert(taskDTO, "task"), taskDTO,
                                builder -> builder
                                                .with(f -> f.setExtra(
                                                                ConversionUtils.convert(taskDTO.getExtra(),
                                                                                "cbor")))
                                                .with(f -> f.setSpec(
                                                                ConversionUtils.convert(taskDTO.getSpec(),
                                                                                "cbor"))));
        }

        /**
         * Update a Task
         * if element is not passed it override causing empty field
         * 
         * @param task
         * @return
         */
        public Task update(Task task, TaskDTO taskDTO) {
                return EntityFactory.combine(
                                task, taskDTO, builder -> builder
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

                                                                                "cbor"))));
        }
}