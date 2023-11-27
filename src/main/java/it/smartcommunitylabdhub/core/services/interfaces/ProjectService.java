package it.smartcommunitylabdhub.core.services.interfaces;

import it.smartcommunitylabdhub.core.models.entities.artifact.ArtifactDTO;
import it.smartcommunitylabdhub.core.models.entities.function.Function;
import it.smartcommunitylabdhub.core.models.entities.project.ProjectDTO;
import it.smartcommunitylabdhub.core.models.entities.workflow.WorkflowDTO;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;

import java.util.List;

public interface ProjectService {

    Page<ProjectDTO> getProjects(Pageable pageable);

    ProjectDTO createProject(ProjectDTO projectDTO);

    ProjectDTO getProject(String uuidOrName);

    ProjectDTO updateProject(ProjectDTO projectDTO, String uuidOrName);

    boolean deleteProject(String uuidOrName);

    boolean deleteProjectByName(String name);

    List<Function> getProjectFunctions(String uuidOrName);

    List<ArtifactDTO> getProjectArtifacts(String uuidOrName);

    List<WorkflowDTO> getProjectWorkflows(String uuidOrName);

}
