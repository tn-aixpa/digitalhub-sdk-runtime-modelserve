package it.smartcommunitylabdhub.core.models.builders.entities;

import org.springframework.stereotype.Component;

import it.smartcommunitylabdhub.core.models.builders.EntityFactory;
import it.smartcommunitylabdhub.core.models.converters.ConversionUtils;
import it.smartcommunitylabdhub.core.models.entities.project.Project;
import it.smartcommunitylabdhub.core.models.entities.project.ProjectDTO;
import it.smartcommunitylabdhub.core.models.enums.State;

@Component
public class ProjectEntityBuilder {

        /**
         * Build a project from a projectDTO and store extra values as a cbor
         * 
         * @return
         */
        public Project build(ProjectDTO projectDTO) {
                return EntityFactory.combine(
                                ConversionUtils.convert(projectDTO, "project"), projectDTO,
                                builder -> builder
                                                .with(p -> p.setExtra(
                                                                ConversionUtils.convert(projectDTO
                                                                                .getExtra(),
                                                                                "cbor")))
                                                .with(p -> p.setMetadata(
                                                                ConversionUtils.convert(projectDTO
                                                                                .getMetadata(),
                                                                                "metadata")))

                );
        }

        /**
         * Update a project if element is not passed it override causing empty field
         * 
         * @param project
         * @return
         */
        public Project update(Project project, ProjectDTO projectDTO) {
                return EntityFactory.combine(
                                project, projectDTO, builder -> builder
                                                .with(p -> p.setDescription(
                                                                projectDTO.getDescription()))
                                                .with(p -> p.setSource(projectDTO.getSource()))
                                                .with(p -> p.setState(projectDTO.getState() == null
                                                                ? State.CREATED
                                                                : State.valueOf(projectDTO
                                                                                .getState())))
                                                .with(p -> p.setExtra(
                                                                ConversionUtils.convert(projectDTO
                                                                                .getExtra(),
                                                                                "cbor")))
                                                .with(p -> p.setMetadata(
                                                                ConversionUtils.convert(projectDTO
                                                                                .getMetadata(),
                                                                                "metadata"))));
        }
}
