package it.smartcommunitylabdhub.core.services.interfaces;

import it.smartcommunitylabdhub.core.models.entities.run.Run;
import it.smartcommunitylabdhub.core.models.entities.workflow.Workflow;
import java.util.List;

import org.springframework.data.domain.Pageable;

public interface WorkflowService {
    List<Workflow> getWorkflows(Pageable pageable);

    Workflow createWorkflow(Workflow workflowDTO);

    Workflow getWorkflow(String uuid);

    Workflow updateWorkflow(Workflow workflowDTO, String uuid);

    boolean deleteWorkflow(String uuid);

    List<Run> getWorkflowRuns(String uuid);
}
