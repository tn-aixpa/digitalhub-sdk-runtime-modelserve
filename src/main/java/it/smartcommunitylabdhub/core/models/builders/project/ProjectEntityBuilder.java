package it.smartcommunitylabdhub.core.models.builders.project;

import it.smartcommunitylabdhub.core.components.infrastructure.factories.specs.SpecEntity;
import it.smartcommunitylabdhub.core.components.infrastructure.factories.specs.SpecRegistry;
import it.smartcommunitylabdhub.core.models.base.interfaces.Spec;
import it.smartcommunitylabdhub.core.models.builders.EntityFactory;
import it.smartcommunitylabdhub.core.models.converters.ConversionUtils;
import it.smartcommunitylabdhub.core.models.entities.project.Project;
import it.smartcommunitylabdhub.core.models.entities.project.ProjectDTO;
import it.smartcommunitylabdhub.core.models.entities.project.specs.ProjectBaseSpec;
import it.smartcommunitylabdhub.core.models.enums.State;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

import java.util.Map;

@Component
public class ProjectEntityBuilder {

    @Autowired
    SpecRegistry<? extends Spec> specRegistry;

    /**
     * Build a project from a projectDTO and store extra values as a cbor
     *
     * @param projectDTO the Project DTO To convert
     * @return Project
     */
    public Project build(ProjectDTO projectDTO) {


        // Retrieve object spec
        ProjectBaseSpec projectSpec = (ProjectBaseSpec) specRegistry.createSpec(
                "project",
                SpecEntity.PROJECT,
                projectDTO.getSpec());

        Map<String, Object> spec = projectSpec.toMap();

        return EntityFactory.combine(
                ConversionUtils.convert(projectDTO, "project"), projectDTO,
                builder -> builder
                        .with(p -> p.setExtra(
                                ConversionUtils.convert(projectDTO
                                                .getExtra(),
                                        "cbor")))
                        .with(p -> {
                            spec.remove("functions");
                            spec.remove("workflows");
                            spec.remove("artifacts");
                            spec.remove("dataitems");
                            p.setSpec(ConversionUtils.convert(spec, "cbor"));
                        })
                        .with(p -> p.setMetadata(
                                ConversionUtils.convert(projectDTO
                                                .getMetadata(),
                                        "metadata")))

        );
    }

    /**
     * Update a project if element is not passed it override causing empty field
     *
     * @param project    entity
     * @param projectDTO the DTO to combine with the project entity
     * @return Project
     */
    public Project update(Project project, ProjectDTO projectDTO) {

        // Retrieve object spec
        ProjectBaseSpec projectSpec = (ProjectBaseSpec) specRegistry.createSpec(
                "project",
                SpecEntity.PROJECT,
                projectDTO.getSpec());

        Map<String, Object> spec = projectSpec.toMap();

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
                        .with(p -> {
                            spec.remove("functions");
                            spec.remove("workflows");
                            spec.remove("artifacts");
                            spec.remove("dataitems");
                            p.setSpec(ConversionUtils.convert(spec, "cbor"));
                        })
                        .with(p -> p.setMetadata(
                                ConversionUtils.convert(projectDTO
                                                .getMetadata(),
                                        "metadata"))));
    }
}
