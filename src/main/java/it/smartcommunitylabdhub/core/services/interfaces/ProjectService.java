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

    ProjectDTO getProject(String uuid);

    ProjectDTO updateProject(ProjectDTO projectDTO, String uuid);

    boolean deleteProject(String uuid);

    boolean deleteProjectByName(String name);

    List<FunctionDTO> getProjectFunctions(String uuid);

    List<ArtifactDTO> getProjectArtifacts(String uuid);

    List<WorkflowDTO> getProjectWorkflows(String uuid);

}
