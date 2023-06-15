package it.smartcommunitylabdhub.core.models.builders.dtos;

import java.util.Optional;

import it.smartcommunitylabdhub.core.models.builders.EntityFactory;
import it.smartcommunitylabdhub.core.models.converters.ConversionUtils;
import it.smartcommunitylabdhub.core.models.dtos.WorkflowDTO;
import it.smartcommunitylabdhub.core.models.entities.Workflow;
import it.smartcommunitylabdhub.core.models.enums.State;

public class WorkflowDTOBuilder {

        private Workflow workflow;
        private boolean embeddable;

        public WorkflowDTOBuilder(
                        Workflow workflow,
                        boolean embeddable) {
                this.workflow = workflow;
                this.embeddable = embeddable;
        }

        public WorkflowDTO build() {
                return EntityFactory.create(WorkflowDTO::new, workflow, builder -> {
                        builder
                                        .with(dto -> dto.setId(workflow.getId()))
                                        .with(dto -> dto.setKind(workflow.getKind()))
                                        .with(dto -> dto.setProject(workflow.getProject()))
                                        .with(dto -> dto.setName(workflow.getName()))

                                        .withIfElse(embeddable, (dto, condition) -> {
                                                Optional.ofNullable(workflow.getEmbedded())
                                                                .filter(embedded -> !condition
                                                                                || (condition && embedded))
                                                                .ifPresent(embedded -> dto
                                                                                .setSpec(ConversionUtils.reverse(
                                                                                                workflow.getSpec(),

                                                                                                "cbor")));
                                        })
                                        .withIfElse(embeddable, (dto, condition) -> {
                                                Optional.ofNullable(workflow.getEmbedded())
                                                                .filter(embedded -> !condition
                                                                                || (condition && embedded))
                                                                .ifPresent(embedded -> dto
                                                                                .setExtra(ConversionUtils.reverse(
                                                                                                workflow.getExtra(),

                                                                                                "cbor")));
                                        })
                                        .withIfElse(embeddable, (dto, condition) -> {
                                                Optional.ofNullable(workflow.getEmbedded())
                                                                .filter(embedded -> !condition
                                                                                || (condition && embedded))
                                                                .ifPresent(embedded -> dto
                                                                                .setCreated(workflow.getCreated()));
                                        })
                                        .withIfElse(embeddable, (dto, condition) -> {
                                                Optional.ofNullable(workflow.getEmbedded())
                                                                .filter(embedded -> !condition
                                                                                || (condition && embedded))
                                                                .ifPresent(embedded -> dto
                                                                                .setUpdated(workflow.getUpdated()));
                                        })
                                        .withIfElse(embeddable, (dto, condition) -> {
                                                Optional.ofNullable(workflow.getEmbedded())
                                                                .filter(embedded -> !condition
                                                                                || (condition && embedded))
                                                                .ifPresent(embedded -> dto
                                                                                .setEmbedded(workflow.getEmbedded()));
                                        })
                                        .withIfElse(embeddable, (dto, condition) -> {

                                                Optional.ofNullable(workflow.getEmbedded())
                                                                .filter(embedded -> !condition
                                                                                || (condition && embedded))
                                                                .ifPresent(embedded -> dto
                                                                                .setState(workflow.getState() == null
                                                                                                ? State.CREATED.name()
                                                                                                : workflow.getState()
                                                                                                                .name()));

                                        });

                });
        }
}