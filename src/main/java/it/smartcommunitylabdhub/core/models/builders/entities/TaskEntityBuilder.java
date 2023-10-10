package it.smartcommunitylabdhub.core.models.builders.entities;

import org.springframework.stereotype.Component;

import it.smartcommunitylabdhub.core.models.builders.EntityFactory;
import it.smartcommunitylabdhub.core.models.converters.ConversionUtils;
import it.smartcommunitylabdhub.core.models.entities.task.Task;
import it.smartcommunitylabdhub.core.models.entities.task.TaskDTO;
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
         * @return
         */
        public Task update(Task task, TaskDTO taskDTO) {
                return EntityFactory.combine(
                                task, taskDTO, builder -> builder
                                                .with(t -> t.setFunction(taskDTO.getFunction()))
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
