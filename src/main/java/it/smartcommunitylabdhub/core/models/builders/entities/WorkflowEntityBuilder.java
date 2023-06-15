package it.smartcommunitylabdhub.core.models.builders.entities;

import it.smartcommunitylabdhub.core.models.builders.EntityFactory;
import it.smartcommunitylabdhub.core.models.converters.ConversionUtils;
import it.smartcommunitylabdhub.core.models.dtos.WorkflowDTO;
import it.smartcommunitylabdhub.core.models.entities.Workflow;
import it.smartcommunitylabdhub.core.models.enums.State;

public class WorkflowEntityBuilder {

        private WorkflowDTO workflowDTO;

        public WorkflowEntityBuilder(
                        WorkflowDTO workflowDTO) {
                this.workflowDTO = workflowDTO;
        }

        /**
         * Build a workflow from a workflowDTO and store extra values as a cbor
         * 
         * @return
         */
        public Workflow build() {
                Workflow workflow = EntityFactory.combine(
                                ConversionUtils.convert(workflowDTO, "workflow"), workflowDTO,
                                builder -> {
                                        builder
                                                        .with(w -> w.setExtra(
                                                                        ConversionUtils.convert(workflowDTO.getExtra(),

                                                                                        "cbor")))
                                                        .with(w -> w.setSpec(
                                                                        ConversionUtils.convert(workflowDTO.getSpec(),

                                                                                        "cbor")));
                                });

                return workflow;
        }

        /**
         * Update a workflow
         * TODO: x because if element is not passed it override causing empty field
         * 
         * @param workflow
         * @return
         */
        public Workflow update(Workflow workflow) {
                return EntityFactory.combine(
                                workflow, workflowDTO, builder -> {
                                        builder
                                                        .with(w -> w.setKind(workflowDTO.getKind()))
                                                        .with(w -> w.setProject(workflowDTO.getProject()))
                                                        .with(w -> w.setState(workflowDTO.getState() == null
                                                                        ? State.CREATED
                                                                        : State.valueOf(workflowDTO.getState())))
                                                        .with(w -> w.setExtra(
                                                                        ConversionUtils.convert(workflowDTO.getExtra(),

                                                                                        "cbor")))
                                                        .with(w -> w.setSpec(
                                                                        ConversionUtils.convert(workflowDTO.getSpec(),

                                                                                        "cbor")))
                                                        .with(w -> w.setEmbedded(workflowDTO.getEmbedded()));
                                });
        }
}