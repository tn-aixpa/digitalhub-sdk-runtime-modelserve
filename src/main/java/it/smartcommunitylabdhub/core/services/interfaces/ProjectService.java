package it.smartcommunitylabdhub.core.services.interfaces;

import java.util.List;

import org.springframework.data.domain.Pageable;

import it.smartcommunitylabdhub.core.models.dtos.ArtifactDTO;
import it.smartcommunitylabdhub.core.models.dtos.FunctionDTO;
import it.smartcommunitylabdhub.core.models.dtos.ProjectDTO;
import it.smartcommunitylabdhub.core.models.dtos.WorkflowDTO;

public interface ProjectService {

    List<ProjectDTO> getProjects(Pageable pageable);

    ProjectDTO createProject(ProjectDTO projectDTO);

    ProjectDTO getProject(String uuidOrName);

    ProjectDTO updateProject(ProjectDTO projectDTO, String uuidOrName);

    boolean deleteProject(String uuidOrName);

    boolean deleteProjectByName(String name);

    List<FunctionDTO> getProjectFunctions(String uuidOrName);

    List<ArtifactDTO> getProjectArtifacts(String uuidOrName);

    List<WorkflowDTO> getProjectWorkflows(String uuidOrName);

}
