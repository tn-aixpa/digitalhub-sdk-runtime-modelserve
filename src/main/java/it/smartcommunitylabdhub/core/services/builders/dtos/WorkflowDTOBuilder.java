package it.smartcommunitylabdhub.core.services.builders.dtos;

import it.smartcommunitylabdhub.core.models.converters.CommandFactory;
import it.smartcommunitylabdhub.core.models.converters.ConversionUtils;
import it.smartcommunitylabdhub.core.models.dtos.WorkflowDTO;
import it.smartcommunitylabdhub.core.models.entities.Workflow;
import it.smartcommunitylabdhub.core.models.enums.State;
import it.smartcommunitylabdhub.core.services.factory.EntityFactory;

public class WorkflowDTOBuilder {

        private CommandFactory commandFactory;
        private Workflow workflow;

        public WorkflowDTOBuilder(
                        CommandFactory commandFactory,
                        Workflow workflow) {
                this.workflow = workflow;
                this.commandFactory = commandFactory;
        }

        public WorkflowDTO build() {
                return EntityFactory.create(WorkflowDTO::new, workflow, builder -> {
                        builder
                                        .with(dto -> dto.setId(workflow.getId()))
                                        .with(dto -> dto.setKind(workflow.getKind()))
                                        .with(dto -> dto.setProject(workflow.getProject()))
                                        .with(dto -> dto.setName(workflow.getName()))
                                        .withIf(workflow.getEmbedded(), dto -> dto.setSpec(ConversionUtils.reverse(
                                                        workflow.getSpec(),
                                                        commandFactory,
                                                        "cbor")))
                                        .withIf(workflow.getEmbedded(), dto -> dto.setExtra(ConversionUtils.reverse(
                                                        workflow.getExtra(),
                                                        commandFactory,
                                                        "cbor")))
                                        .with(dto -> dto.setState(workflow.getState() == null ? State.CREATED.name()
                                                        : workflow.getState().name()))
                                        .with(dto -> dto.setCreated(workflow.getCreated()))
                                        .with(dto -> dto.setUpdated(workflow.getUpdated()))
                                        .with(dto -> dto.setEmbedded(workflow.getEmbedded()))
                                        .with(dto -> dto.setState(workflow.getState() == null ? State.CREATED.name()
                                                        : workflow.getState().name()));

                });
        }
}