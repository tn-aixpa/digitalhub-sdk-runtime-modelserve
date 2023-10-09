package it.smartcommunitylabdhub.core.services;

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
import it.smartcommunitylabdhub.core.models.builders.dtos.ArtifactDTOBuilder;
import it.smartcommunitylabdhub.core.models.builders.dtos.FunctionDTOBuilder;
import it.smartcommunitylabdhub.core.models.builders.dtos.ProjectDTOBuilder;
import it.smartcommunitylabdhub.core.models.builders.dtos.WorkflowDTOBuilder;
import it.smartcommunitylabdhub.core.models.builders.entities.ProjectEntityBuilder;
import it.smartcommunitylabdhub.core.models.entities.artifact.Artifact;
import it.smartcommunitylabdhub.core.models.entities.artifact.ArtifactDTO;
import it.smartcommunitylabdhub.core.models.entities.function.Function;
import it.smartcommunitylabdhub.core.models.entities.function.FunctionDTO;
import it.smartcommunitylabdhub.core.models.entities.project.Project;
import it.smartcommunitylabdhub.core.models.entities.project.ProjectDTO;
import it.smartcommunitylabdhub.core.models.entities.workflow.Workflow;
import it.smartcommunitylabdhub.core.models.entities.workflow.WorkflowDTO;
import it.smartcommunitylabdhub.core.repositories.ArtifactRepository;
import it.smartcommunitylabdhub.core.repositories.DataItemRepository;
import it.smartcommunitylabdhub.core.repositories.FunctionRepository;
import it.smartcommunitylabdhub.core.repositories.LogRepository;
import it.smartcommunitylabdhub.core.repositories.ProjectRepository;
import it.smartcommunitylabdhub.core.repositories.RunRepository;
import it.smartcommunitylabdhub.core.repositories.TaskRepository;
import it.smartcommunitylabdhub.core.repositories.WorkflowRepository;
import it.smartcommunitylabdhub.core.services.interfaces.ProjectService;
import jakarta.transaction.Transactional;

@Service
public class ProjectServiceImpl implements ProjectService {
    @Autowired
    ProjectRepository projectRepository;

    @Autowired
    FunctionRepository functionRepository;

    @Autowired
    ArtifactRepository artifactRepository;

    @Autowired
    WorkflowRepository workflowRepository;

    @Autowired
    DataItemRepository dataItemRepository;

    @Autowired
    LogRepository logRepository;

    @Autowired
    RunRepository runRepository;

    @Autowired
    TaskRepository taskRepository;

    @Autowired
    ProjectDTOBuilder projectDTOBuilder;

    @Autowired
    ProjectEntityBuilder projectEntityBuilder;

    @Autowired
    ArtifactDTOBuilder artifactDTOBuilder;

    @Autowired
    FunctionDTOBuilder functionDTOBuilder;

    @Autowired
    WorkflowDTOBuilder workflowDTOBuilder;

    @Override
    public ProjectDTO getProject(String uuidOrName) {

        return projectRepository.findById(uuidOrName)
                .or(() -> projectRepository.findByName(uuidOrName))
                .map(project -> {
                    List<Function> functions = functionRepository.findByProject(project.getName());
                    List<Artifact> artifacts = artifactRepository.findByProject(project.getName());
                    List<Workflow> workflows = workflowRepository.findByProject(project.getName());

                    return projectDTOBuilder.build(project, artifacts, functions, workflows, true);
                })
                .orElseThrow(() -> new CoreException(
                        "ProjectNotFound",
                        "The project you are searching for does not exist.",
                        HttpStatus.NOT_FOUND));
    }

    @Override
    public List<ProjectDTO> getProjects(Pageable pageable) {
        try {
            Page<Project> projectPage = this.projectRepository.findAll(pageable);
            return projectPage.getContent().stream().map((project) -> {
                List<Function> functions = functionRepository.findByProject(project.getName());
                List<Artifact> artifacts = artifactRepository.findByProject(project.getName());
                List<Workflow> workflows = workflowRepository.findByProject(project.getName());

                return projectDTOBuilder.build(project, artifacts, functions, workflows, true);
            }).collect(Collectors.toList());
        } catch (CustomException e) {
            throw new CoreException(
                    "InternalServerError",
                    e.getMessage(),
                    HttpStatus.INTERNAL_SERVER_ERROR);
        }

    }

    @Override
    public ProjectDTO createProject(ProjectDTO projectDTO) {
        if ((projectDTO.getId() != null && projectRepository.existsById(projectDTO.getId())) ||
                projectRepository.existsByName(projectDTO.getName())) {
            throw new CoreException("DuplicateProjectIdOrName",
                    "Cannot create the project, duplicated Id or Name",
                    HttpStatus.INTERNAL_SERVER_ERROR);
        }
        return Optional.of(projectEntityBuilder.build(projectDTO))
                .map(project -> {
                    projectRepository.save(project);
                    return projectDTOBuilder.build(project, List.of(), List.of(), List.of(), true);
                })
                .orElseThrow(() -> new CoreException(
                        "InternalServerError",
                        "Failed to generate the project.",
                        HttpStatus.INTERNAL_SERVER_ERROR));

    }

    @Override
    public ProjectDTO updateProject(ProjectDTO projectDTO, String uuidOrName) {

        return Optional.ofNullable(projectDTO.getId())
                .filter(id -> id.equals(uuidOrName))
                .or(() -> Optional.ofNullable(projectDTO.getName())
                        .filter(name -> name.equals(uuidOrName)))
                .map(id -> projectRepository.findById(uuidOrName)
                        .or(() -> projectRepository.findByName(uuidOrName))
                        .orElseThrow(() -> new CoreException(
                                "ProjectNotFound",
                                "The project you are searching for does not exist.",
                                HttpStatus.NOT_FOUND)))
                .map(project -> {
                    final Project projectUpdated = projectEntityBuilder.update(project, projectDTO);
                    this.projectRepository.save(projectUpdated);

                    List<Function> functions =
                            functionRepository.findByProject(projectUpdated.getName());
                    List<Artifact> artifacts =
                            artifactRepository.findByProject(projectUpdated.getName());
                    List<Workflow> workflows =
                            workflowRepository.findByProject(projectUpdated.getName());

                    return projectDTOBuilder.build(projectUpdated, artifacts, functions, workflows,
                            true);
                })
                .orElseThrow(() -> new CoreException(
                        "ProjectNotMatch",
                        "Trying to update a project with a UUID different from the one passed in the request.",
                        HttpStatus.NOT_FOUND));

    }

    @Override
    @Transactional
    public boolean deleteProject(String uuidOrName) {
        return Optional.ofNullable(uuidOrName)
                .map(value -> {
                    boolean deleted = false;
                    if (projectRepository.existsById(value)) {
                        projectRepository.findById(value).ifPresent(project -> {
                            // delete functions, artifacts, workflow, dataitems
                            this.artifactRepository.deleteByProjectName(project.getName());
                            this.dataItemRepository.deleteByProjectName(project.getName());
                            this.workflowRepository.deleteByProjectName(project.getName());
                            this.functionRepository.deleteByProjectName(project.getName());
                            this.logRepository.deleteByProjectName(project.getName());
                            this.runRepository.deleteByProjectName(project.getName());
                            this.taskRepository.deleteByProjectName(project.getName());
                        });
                        projectRepository.deleteById(value);
                        deleted = true;
                    } else if (projectRepository.existsByName(value)) {
                        projectRepository.findByName(value).ifPresent(project -> {
                            // delete functions, artifacts, workflow, dataitems
                            this.artifactRepository.deleteByProjectName(project.getName());
                            this.dataItemRepository.deleteByProjectName(project.getName());
                            this.workflowRepository.deleteByProjectName(project.getName());
                            this.functionRepository.deleteByProjectName(project.getName());
                            this.logRepository.deleteByProjectName(project.getName());
                            this.runRepository.deleteByProjectName(project.getName());
                            this.taskRepository.deleteByProjectName(project.getName());
                        });
                        projectRepository.deleteByName(value);
                        deleted = true;
                    }
                    if (!deleted) {
                        throw new CoreException(
                                "ProjectNotFound",
                                "The project you are trying to delete does not exist.",
                                HttpStatus.NOT_FOUND);
                    }
                    return deleted;
                })
                .orElseThrow(() -> new CoreException(
                        "InternalServerError",
                        "Cannot delete project",
                        HttpStatus.INTERNAL_SERVER_ERROR));
    }

    @Override
    public List<FunctionDTO> getProjectFunctions(String uuidOrName) {

        return Optional.ofNullable(projectRepository.findById(uuidOrName)
                .or(() -> projectRepository.findByName(uuidOrName)))
                .orElseThrow(() -> new CoreException(
                        "ProjectNotFound",
                        "The project you are searching for does not exist.",
                        HttpStatus.NOT_FOUND))
                .map(Project::getName)
                .flatMap(projectName -> {
                    try {
                        List<Function> functions = functionRepository.findByProject(projectName);
                        return Optional.of(
                                functions.stream()
                                        .map(function -> functionDTOBuilder.build(function, false))
                                        .collect(Collectors.toList()));
                    } catch (CustomException e) {
                        throw new CoreException(
                                "InternalServerError",
                                e.getMessage(),
                                HttpStatus.INTERNAL_SERVER_ERROR);
                    }
                })
                .orElseThrow(() -> new CoreException(
                        "InternalServerError",
                        "Error occurred while retrieving functions.",
                        HttpStatus.INTERNAL_SERVER_ERROR));

    }

    @Override
    public List<ArtifactDTO> getProjectArtifacts(String uuidOrName) {
        return Optional.ofNullable(projectRepository.findById(uuidOrName)
                .or(() -> projectRepository.findByName(uuidOrName)))
                .orElseThrow(() -> new CoreException(
                        "ProjectNotFound",
                        "The project you are searching for does not exist.",
                        HttpStatus.NOT_FOUND))
                .map(Project::getName)
                .flatMap(projectName -> {
                    try {
                        List<Artifact> artifacts = artifactRepository.findByProject(projectName);
                        return Optional.of(
                                artifacts.stream().map(
                                        artifact -> artifactDTOBuilder.build(artifact, false))
                                        .collect(Collectors.toList()));
                    } catch (CustomException e) {
                        throw new CoreException(
                                "InternalServerError",
                                e.getMessage(),
                                HttpStatus.INTERNAL_SERVER_ERROR);
                    }
                })
                .orElseThrow(() -> new CoreException(
                        "InternalServerError",
                        "Error occurred while retrieving artifacts.",
                        HttpStatus.INTERNAL_SERVER_ERROR));

    }

    @Override
    public List<WorkflowDTO> getProjectWorkflows(String uuidOrName) {
        return Optional.ofNullable(projectRepository.findById(uuidOrName)
                .or(() -> projectRepository.findByName(uuidOrName)))
                .orElseThrow(() -> new CoreException(
                        "ProjectNotFound",
                        "The project you are searching for does not exist.",
                        HttpStatus.NOT_FOUND))
                .map(Project::getName)
                .flatMap(projectName -> {
                    try {
                        List<Workflow> workflows = workflowRepository.findByProject(projectName);
                        return Optional.of(
                                workflows.stream()
                                        .map(workflow -> workflowDTOBuilder.build(workflow, false))
                                        .collect(Collectors.toList()));
                    } catch (CustomException e) {
                        throw new CoreException(
                                "InternalServerError",
                                e.getMessage(),
                                HttpStatus.INTERNAL_SERVER_ERROR);
                    }
                })
                .orElseThrow(() -> new CoreException(
                        "InternalServerError",
                        "Error occurred while retrieving workflows.",
                        HttpStatus.INTERNAL_SERVER_ERROR));
    }

    @Override
    public boolean deleteProjectByName(String name) {
        try {
            if (this.projectRepository.existsByName(name)) {
                this.projectRepository.deleteByName(name);
                return true;
            }
            return false;
        } catch (Exception e) {
            throw new CoreException(
                    "InternalServerError",
                    "cannot delete project",
                    HttpStatus.INTERNAL_SERVER_ERROR);
        }
    }

}
