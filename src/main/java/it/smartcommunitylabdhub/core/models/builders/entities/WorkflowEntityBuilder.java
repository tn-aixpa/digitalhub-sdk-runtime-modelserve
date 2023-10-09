package it.smartcommunitylabdhub.core.models.builders.entities;

import org.springframework.stereotype.Component;

import it.smartcommunitylabdhub.core.models.builders.EntityFactory;
import it.smartcommunitylabdhub.core.models.converters.ConversionUtils;
import it.smartcommunitylabdhub.core.models.entities.workflow.Workflow;
import it.smartcommunitylabdhub.core.models.entities.workflow.WorkflowDTO;
import it.smartcommunitylabdhub.core.models.enums.State;

@Component
public class WorkflowEntityBuilder {

        /**
         * Build a workflow from a workflowDTO and store extra values as a cbor
         * 
         * @return
         */
        public Workflow build(WorkflowDTO workflowDTO) {
                return EntityFactory.combine(
                                ConversionUtils.convert(workflowDTO, "workflow"), workflowDTO,
                                builder -> builder
                                                .with(w -> w.setExtra(
                                                                ConversionUtils.convert(workflowDTO
                                                                                .getExtra(),

                                                                                "cbor")))
                                                .with(w -> w.setSpec(
                                                                ConversionUtils.convert(workflowDTO
                                                                                .getSpec(),

                                                                                "cbor"))));

        }

        /**
         * Update a workflow if element is not passed it override causing empty field
         * 
         * @param workflow
         * @return
         */
        public Workflow update(Workflow workflow, WorkflowDTO workflowDTO) {
                return EntityFactory.combine(
                                workflow, workflowDTO, builder -> builder
                                                .with(w -> w.setKind(workflowDTO.getKind()))
                                                .with(w -> w.setProject(workflowDTO.getProject()))
                                                .with(w -> w.setState(workflowDTO.getState() == null
                                                                ? State.CREATED
                                                                : State.valueOf(workflowDTO
                                                                                .getState())))
                                                .with(w -> w.setExtra(
                                                                ConversionUtils.convert(workflowDTO
                                                                                .getExtra(),

                                                                                "cbor")))
                                                .with(w -> w.setSpec(
                                                                ConversionUtils.convert(workflowDTO
                                                                                .getSpec(),

                                                                                "cbor")))
                                                .with(w -> w.setEmbedded(
                                                                workflowDTO.getEmbedded())));
        }
}
