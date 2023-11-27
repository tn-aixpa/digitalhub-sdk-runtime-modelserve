package it.smartcommunitylabdhub.core.services.context.interfaces;

import it.smartcommunitylabdhub.core.models.entities.workflow.WorkflowDTO;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;

public interface WorkflowContextService {

    WorkflowDTO createWorkflow(String projectName, WorkflowDTO workflowDTO);

    Page<WorkflowDTO> getByProjectNameAndWorkflowName(
            String projectName, String workflowName, Pageable pageable);

    Page<WorkflowDTO> getLatestByProjectName(
            String projectName, Pageable pageable);

    WorkflowDTO getByProjectAndWorkflowAndUuid(
            String projectName, String workflowName, String uuid);

    WorkflowDTO getLatestByProjectNameAndWorkflowName(
            String projectName, String workflowName);

    WorkflowDTO createOrUpdateWorkflow(String projectName, String workflowName,
                                       WorkflowDTO workflowDTO);

    WorkflowDTO updateWorkflow(String projectName, String workflowName, String uuid,
                               WorkflowDTO workflowDTO);

    Boolean deleteSpecificWorkflowVersion(String projectName, String workflowName, String uuid);

    Boolean deleteAllWorkflowVersions(String projectName, String workflowName);
}
