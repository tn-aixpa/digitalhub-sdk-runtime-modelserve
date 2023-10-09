package it.smartcommunitylabdhub.core.models.converters.types;

import org.springframework.stereotype.Component;

import it.smartcommunitylabdhub.core.exceptions.CustomException;
import it.smartcommunitylabdhub.core.models.converters.interfaces.Converter;
import it.smartcommunitylabdhub.core.models.entities.project.Project;
import it.smartcommunitylabdhub.core.models.entities.project.ProjectDTO;
import it.smartcommunitylabdhub.core.models.enums.State;

@Component
public class ProjectConverter implements Converter<ProjectDTO, Project> {

    @Override
    public Project convert(ProjectDTO projectDTO) throws CustomException {
        return Project.builder()
                .id(projectDTO.getId())
                .name(projectDTO.getName())
                .description(projectDTO.getDescription())
                .source(projectDTO.getSource())
                .state(projectDTO.getState() == null ? State.CREATED
                        : State.valueOf(projectDTO.getState()))
                .build();
    }

    @Override
    public ProjectDTO reverseConvert(Project project) throws CustomException {
        return ProjectDTO.builder()
                .id(project.getId())
                .name(project.getName())
                .description(project.getDescription())
                .source(project.getSource())
                .state(project.getState() == null ? State.CREATED.name()
                        : project.getState().name())
                .created(project.getCreated())
                .updated(project.getUpdated())
                .build();
    }

}
