package it.smartcommunitylabdhub.core.services;

import java.util.List;
import java.util.stream.Collectors;

import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Service;

import it.smartcommunitylabdhub.core.exceptions.CoreException;
import it.smartcommunitylabdhub.core.exceptions.CustomException;
import it.smartcommunitylabdhub.core.models.converters.CommandFactory;
import it.smartcommunitylabdhub.core.models.converters.ConversionUtils;
import it.smartcommunitylabdhub.core.models.dtos.ArtifactDTO;
import it.smartcommunitylabdhub.core.models.dtos.FunctionDTO;
import it.smartcommunitylabdhub.core.models.dtos.ProjectDTO;
import it.smartcommunitylabdhub.core.models.dtos.WorkflowDTO;
import it.smartcommunitylabdhub.core.models.entities.Artifact;
import it.smartcommunitylabdhub.core.models.entities.Function;
import it.smartcommunitylabdhub.core.models.entities.Project;
import it.smartcommunitylabdhub.core.models.entities.Workflow;
import it.smartcommunitylabdhub.core.repositories.ArtifactRepository;
import it.smartcommunitylabdhub.core.repositories.FunctionRepository;
import it.smartcommunitylabdhub.core.repositories.ProjectRepository;
import it.smartcommunitylabdhub.core.repositories.WorkflowRepository;
import it.smartcommunitylabdhub.core.services.builders.dtos.ProjectDTOBuilder;
import it.smartcommunitylabdhub.core.services.builders.entities.ProjectEntityBuilder;
import it.smartcommunitylabdhub.core.services.interfaces.ProjectService;

@Service
public class ProjectServiceImpl implements ProjectService {
    private final ProjectRepository projectRepository;
    private final FunctionRepository functionRepository;
    private final ArtifactRepository artifactRepository;
    private final WorkflowRepository workflowRepository;
    private final CommandFactory commandFactory;

    public ProjectServiceImpl(
            ProjectRepository projectRepository, FunctionRepository functionRepository,
            ArtifactRepository artifactRepository, WorkflowRepository workflowRepository,
            CommandFactory commandFactory) {
        this.projectRepository = projectRepository;
        this.functionRepository = functionRepository;
        this.artifactRepository = artifactRepository;
        this.workflowRepository = workflowRepository;
        this.commandFactory = commandFactory;

    }

    @Override
    public ProjectDTO getProject(String uuid) {

        final Project project = projectRepository.findById(uuid).orElse(null);
        if (project == null) {
            throw new CoreException(
                    "ProjectNotFound",
                    "The project you are searching for does not exist.",
                    HttpStatus.NOT_FOUND);
        }

        try {
            List<Function> functions = functionRepository.findByProject(project.getName());
            List<Artifact> artifacts = artifactRepository.findByProject(project.getName());
            List<Workflow> workflows = workflowRepository.findByProject(project.getName());

            return new ProjectDTOBuilder(
                    commandFactory,
                    project,
                    artifacts,
                    functions,
                    workflows).build();

        } catch (CustomException e) {
            throw new CoreException(
                    "InternalServerError",
                    e.getMessage(),
                    HttpStatus.INTERNAL_SERVER_ERROR);
        }
    }

    @Override
    public List<ProjectDTO> getProjects(Pageable pageable) {
        try {
            Page<Project> projectPage = this.projectRepository.findAll(pageable);
            return projectPage.getContent().stream().map((project) -> {
                List<Function> functions = functionRepository.findByProject(project.getName());
                List<Artifact> artifacts = artifactRepository.findByProject(project.getName());
                List<Workflow> workflows = workflowRepository.findByProject(project.getName());

                return new ProjectDTOBuilder(commandFactory, project, artifacts, functions, workflows).build();
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
        try {
            // Build a project and store it on db
            final Project project = new ProjectEntityBuilder(commandFactory, projectDTO).build();

            if (this.projectRepository.existsByName(project.getId())) {
                throw new CustomException("Cannot generate project with an existing project uuid", null);
            }
            this.projectRepository.save(project);

            // Return project DTO
            return new ProjectDTOBuilder(
                    commandFactory,
                    project,
                    List.of(),
                    List.of(),
                    List.of()).build();

        } catch (CustomException e) {
            throw new CoreException(
                    "InternalServerError",
                    e.getMessage(),
                    HttpStatus.INTERNAL_SERVER_ERROR);
        }

    }

    @Override
    public ProjectDTO updateProject(ProjectDTO projectDTO, String uuid) {

        if (!projectDTO.getId().equals(uuid)) {
            throw new CoreException(
                    "ProjectNotMatch",
                    "Trying to update a project with an uuid different from the one passed in the request.",
                    HttpStatus.NOT_FOUND);
        }

        final Project project = projectRepository.findById(uuid).orElse(null);
        if (project == null) {
            throw new CoreException(
                    "ProjectNotFound",
                    "The project you are searching for does not exist.",
                    HttpStatus.NOT_FOUND);
        }

        try {

            ProjectEntityBuilder projectBuilder = new ProjectEntityBuilder(commandFactory, projectDTO);

            final Project projectUpdated = projectBuilder.update(project);
            this.projectRepository.save(projectUpdated);

            // get functions, artifacts and worflows for current projects

            List<Function> functions = functionRepository.findByProject(projectUpdated.getName());
            List<Artifact> artifacts = artifactRepository.findByProject(projectUpdated.getName());
            List<Workflow> workflows = workflowRepository.findByProject(projectUpdated.getName());

            return new ProjectDTOBuilder(
                    commandFactory,
                    projectUpdated,
                    artifacts,
                    functions,
                    workflows).build();

        } catch (CustomException e) {
            throw new CoreException(
                    "InternalServerError",
                    e.getMessage(),
                    HttpStatus.INTERNAL_SERVER_ERROR);
        }
    }

    @Override
    public boolean deleteProject(String uuid) {
        try {
            if (this.projectRepository.existsById(uuid)) {
                this.projectRepository.deleteById(uuid);
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

    @Override
    public List<FunctionDTO> getProjectFunctions(String uuid) {
        final Project project = projectRepository.findById(uuid).orElse(null);
        if (project == null) {
            throw new CoreException(
                    "ProjectNotFound",
                    "The project you are searching for does not exist.",
                    HttpStatus.NOT_FOUND);
        }

        try {
            List<Function> functions = functionRepository.findByProject(project.getName());
            return (List<FunctionDTO>) ConversionUtils.reverseIterable(functions,
                    commandFactory,
                    "function",
                    FunctionDTO.class);

        } catch (CustomException e) {
            throw new CoreException(
                    "InternalServerError",
                    e.getMessage(),
                    HttpStatus.INTERNAL_SERVER_ERROR);
        }
    }

    @Override
    public List<ArtifactDTO> getProjectArtifacts(String uuid) {
        final Project project = projectRepository.findById(uuid).orElse(null);
        if (project == null) {
            throw new CoreException(
                    "ProjectNotFound",
                    "The project you are searching for does not exist.",
                    HttpStatus.NOT_FOUND);
        }

        try {
            List<Artifact> artifacts = artifactRepository.findByProject(project.getName());

            return (List<ArtifactDTO>) ConversionUtils.reverseIterable(artifacts,
                    commandFactory,
                    "artifact",
                    ArtifactDTO.class);

        } catch (CustomException e) {
            throw new CoreException(
                    "InternalServerError",
                    e.getMessage(),
                    HttpStatus.INTERNAL_SERVER_ERROR);
        }
    }

    @Override
    public List<WorkflowDTO> getProjectWorkflows(String uuid) {
        final Project project = projectRepository.findById(uuid).orElse(null);
        if (project == null) {
            throw new CoreException(
                    "ProjectNotFound",
                    "The project you are searching for does not exist.",
                    HttpStatus.NOT_FOUND);
        }

        try {
            List<Workflow> workflows = workflowRepository.findByProject(project.getName());

            return (List<WorkflowDTO>) ConversionUtils.reverseIterable(workflows,
                    commandFactory,
                    "workflow",
                    WorkflowDTO.class);
        } catch (CustomException e) {
            throw new CoreException(
                    "InternalServerError",
                    e.getMessage(),
                    HttpStatus.INTERNAL_SERVER_ERROR);
        }
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
