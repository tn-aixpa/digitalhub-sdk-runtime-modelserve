package it.smartcommunitylabdhub.core.models.converters.types;

import org.springframework.stereotype.Component;

import it.smartcommunitylabdhub.core.exceptions.CustomException;
import it.smartcommunitylabdhub.core.models.converters.interfaces.Converter;
import it.smartcommunitylabdhub.core.models.entities.workflow.Workflow;
import it.smartcommunitylabdhub.core.models.entities.workflow.WorkflowDTO;
import it.smartcommunitylabdhub.core.models.enums.State;

@Component
public class WorkflowConverter implements Converter<WorkflowDTO, Workflow> {

    @Override
    public Workflow convert(WorkflowDTO workflowDTO) throws CustomException {
        return Workflow.builder()
                .id(workflowDTO.getId())
                .name(workflowDTO.getName())
                .kind(workflowDTO.getKind())
                .project(workflowDTO.getProject())
                .embedded(workflowDTO.getEmbedded())
                .state(workflowDTO.getState() == null ? State.CREATED
                        : State.valueOf(workflowDTO.getState()))
                .build();
    }

    @Override
    public WorkflowDTO reverseConvert(Workflow workflow) throws CustomException {
        return WorkflowDTO.builder()
                .id(workflow.getId())
                .name(workflow.getName())
                .kind(workflow.getKind())
                .project(workflow.getProject())
                .embedded(workflow.getEmbedded())
                .state(workflow.getState() == null ? State.CREATED.name()
                        : workflow.getState().name())
                .created(workflow.getCreated())
                .updated(workflow.getUpdated())
                .build();
    }

}
