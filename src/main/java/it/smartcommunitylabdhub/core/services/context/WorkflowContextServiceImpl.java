package it.smartcommunitylabdhub.core.services.context;

import java.util.List;
import java.util.Optional;
import java.util.stream.Collectors;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Service;

import it.smartcommunitylabdhub.core.exceptions.CoreException;
import it.smartcommunitylabdhub.core.exceptions.CustomException;
import it.smartcommunitylabdhub.core.models.dtos.WorkflowDTO;
import it.smartcommunitylabdhub.core.models.entities.Workflow;
import it.smartcommunitylabdhub.core.repositories.WorkflowRepository;
import it.smartcommunitylabdhub.core.models.builders.dtos.WorkflowDTOBuilder;
import it.smartcommunitylabdhub.core.models.builders.entities.WorkflowEntityBuilder;
import it.smartcommunitylabdhub.core.services.context.interfaces.WorkflowContextService;
import jakarta.transaction.Transactional;

@Service
public class WorkflowContextServiceImpl extends ContextService implements WorkflowContextService {

    @Autowired
    WorkflowRepository workflowRepository;

    @Override
    public WorkflowDTO createWorkflow(String projectName, WorkflowDTO workflowDTO) {
        try {
            // Check that project context is the same as the project passed to the
            // workflowDTO
            if (!projectName.equals(workflowDTO.getProject())) {
                throw new CustomException("Project Context and Workflow Project does not match", null);
            }

            // Check project context
            checkContext(workflowDTO.getProject());

            // Check if workflow already exist if exist throw exception otherwise create a
            // new one
            Workflow workflow = (Workflow) Optional.ofNullable(workflowDTO.getId())
                    .flatMap(id -> workflowRepository.findById(id)
                            .map(a -> {
                                throw new CustomException(
                                        "The project already contains an workflow with the specified UUID.", null);
                            }))
                    .orElseGet(() -> {
                        // Build an workflow and store it in the database
                        Workflow newWorkflow = new WorkflowEntityBuilder(workflowDTO).build();
                        return workflowRepository.save(newWorkflow);
                    });

            // Return workflow DTO
            return new WorkflowDTOBuilder(

                    workflow, false).build();

        } catch (CustomException e) {
            throw new CoreException(
                    "InternalServerError",
                    e.getMessage(),
                    HttpStatus.INTERNAL_SERVER_ERROR);
        }
    }

    @Override
    public List<WorkflowDTO> getLatestByProjectName(String projectName, Pageable pageable) {
        try {
            checkContext(projectName);

            Page<Workflow> workflowPage = this.workflowRepository
                    .findAllLatestWorkflowsByProject(projectName,
                            pageable);
            return workflowPage.getContent()
                    .stream()
                    .map((workflow) -> {
                        return new WorkflowDTOBuilder(workflow, false).build();
                    }).collect(Collectors.toList());
        } catch (CustomException e) {
            throw new CoreException(
                    "InternalServerError",
                    e.getMessage(),
                    HttpStatus.INTERNAL_SERVER_ERROR);
        }
    }

    @Override
    public List<WorkflowDTO> getByProjectNameAndWorkflowName(String projectName, String workflowName,
            Pageable pageable) {
        try {
            checkContext(projectName);

            Page<Workflow> workflowPage = this.workflowRepository
                    .findAllByProjectAndNameOrderByCreatedDesc(projectName, workflowName,
                            pageable);
            return workflowPage.getContent()
                    .stream()
                    .map((workflow) -> {
                        return new WorkflowDTOBuilder(workflow, false).build();
                    }).collect(Collectors.toList());
        } catch (CustomException e) {
            throw new CoreException(
                    "InternalServerError",
                    e.getMessage(),
                    HttpStatus.INTERNAL_SERVER_ERROR);
        }

    }

    @Override
    public WorkflowDTO getByProjectAndWorkflowAndUuid(String projectName, String workflowName,
            String uuid) {
        try {
            // Check project context
            checkContext(projectName);

            return this.workflowRepository.findByProjectAndNameAndId(projectName, workflowName, uuid).map(
                    workflow -> new WorkflowDTOBuilder(workflow, false).build())
                    .orElseThrow(
                            () -> new CustomException("The workflow does not exist.", null));

        } catch (CustomException e) {
            throw new CoreException(
                    "InternalServerError",
                    e.getMessage(),
                    HttpStatus.INTERNAL_SERVER_ERROR);
        }
    }

    @Override
    public WorkflowDTO getLatestByProjectNameAndWorkflowName(String projectName, String workflowName) {
        try {
            // Check project context
            checkContext(projectName);

            return this.workflowRepository.findLatestWorkflowByProjectAndName(projectName, workflowName).map(
                    workflow -> new WorkflowDTOBuilder(workflow, false).build())
                    .orElseThrow(
                            () -> new CustomException("The workflow does not exist.", null));

        } catch (CustomException e) {
            throw new CoreException(
                    "InternalServerError",
                    e.getMessage(),
                    HttpStatus.INTERNAL_SERVER_ERROR);
        }
    }

    @Override
    public WorkflowDTO createOrUpdateWorkflow(String projectName, String workflowName, WorkflowDTO workflowDTO) {
        try {
            // Check that project context is the same as the project passed to the
            // workflowDTO
            if (!projectName.equals(workflowDTO.getProject())) {
                throw new CustomException("Project Context and Workflow Project does not match.", null);
            }
            if (!workflowName.equals(workflowDTO.getName())) {
                throw new CustomException(
                        "Trying to create/update an workflow with name different from the one passed in the request.",
                        null);
            }

            // Check project context
            checkContext(workflowDTO.getProject());

            // Check if workflow already exist if exist throw exception otherwise create a
            // new one
            Workflow workflow = Optional.ofNullable(workflowDTO.getId())
                    .flatMap(id -> {
                        Optional<Workflow> optionalWorkflow = workflowRepository.findById(id);
                        if (optionalWorkflow.isPresent()) {
                            Workflow existingWorkflow = optionalWorkflow.get();

                            // Update the existing workflow version
                            WorkflowEntityBuilder workflowBuilder = new WorkflowEntityBuilder(
                                    workflowDTO);
                            final Workflow workflowUpdated = workflowBuilder.update(existingWorkflow);
                            return Optional.of(this.workflowRepository.save(workflowUpdated));

                        } else {
                            // Build a new workflow and store it in the database
                            Workflow newWorkflow = new WorkflowEntityBuilder(workflowDTO).build();
                            return Optional.of(workflowRepository.save(newWorkflow));
                        }
                    })
                    .orElseGet(() -> {
                        // Build a new workflow and store it in the database
                        Workflow newWorkflow = new WorkflowEntityBuilder(workflowDTO).build();
                        return workflowRepository.save(newWorkflow);
                    });

            // Return workflow DTO
            return new WorkflowDTOBuilder(

                    workflow, false).build();

        } catch (CustomException e) {
            throw new CoreException(
                    "InternalServerError",
                    e.getMessage(),
                    HttpStatus.INTERNAL_SERVER_ERROR);
        }
    }

    @Override
    public WorkflowDTO updateWorkflow(String projectName, String workflowName, String uuid, WorkflowDTO workflowDTO) {

        try {
            // Check that project context is the same as the project passed to the
            // workflowDTO
            if (!projectName.equals(workflowDTO.getProject())) {
                throw new CustomException("Project Context and Workflow Project does not match", null);
            }
            if (!uuid.equals(workflowDTO.getId())) {
                throw new CustomException(
                        "Trying to update an workflow with an ID different from the one passed in the request.", null);
            }
            // Check project context
            checkContext(workflowDTO.getProject());

            Workflow workflow = this.workflowRepository.findById(workflowDTO.getId()).map(
                    a -> {
                        // Update the existing workflow version
                        WorkflowEntityBuilder workflowBuilder = new WorkflowEntityBuilder(
                                workflowDTO);
                        return workflowBuilder.update(a);
                    })
                    .orElseThrow(
                            () -> new CustomException("The workflow does not exist.", null));

            // Return workflow DTO
            return new WorkflowDTOBuilder(

                    workflow, false).build();

        } catch (CustomException e) {
            throw new CoreException(
                    "InternalServerError",
                    e.getMessage(),
                    HttpStatus.INTERNAL_SERVER_ERROR);
        }
    }

    @Override
    @Transactional
    public Boolean deleteSpecificWorkflowVersion(String projectName, String workflowName, String uuid) {
        try {
            if (this.workflowRepository.existsByProjectAndNameAndId(projectName, workflowName, uuid)) {
                this.workflowRepository.deleteByProjectAndNameAndId(projectName, workflowName, uuid);
                return true;
            }
            throw new CoreException(
                    "WorkflowNotFound",
                    "The workflow you are trying to delete does not exist.",
                    HttpStatus.NOT_FOUND);
        } catch (Exception e) {
            throw new CoreException(
                    "InternalServerError",
                    "cannot delete workflow",
                    HttpStatus.INTERNAL_SERVER_ERROR);
        }
    }

    @Override
    @Transactional
    public Boolean deleteAllWorkflowVersions(String projectName, String workflowName) {
        try {
            if (workflowRepository.existsByProjectAndName(projectName, workflowName)) {
                this.workflowRepository.deleteByProjectAndName(projectName, workflowName);
                return true;
            }
            throw new CoreException(
                    "WorkflowNotFound",
                    "The workflows you are trying to delete does not exist.",
                    HttpStatus.NOT_FOUND);
        } catch (Exception e) {
            throw new CoreException(
                    "InternalServerError",
                    "cannot delete workflow",
                    HttpStatus.INTERNAL_SERVER_ERROR);
        }
    }
}
