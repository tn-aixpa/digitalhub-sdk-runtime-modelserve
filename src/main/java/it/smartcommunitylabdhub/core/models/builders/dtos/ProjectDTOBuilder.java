package it.smartcommunitylabdhub.core.models.builders.dtos;

import java.util.List;
import java.util.stream.Collectors;

import it.smartcommunitylabdhub.core.models.builders.EntityFactory;
import it.smartcommunitylabdhub.core.models.converters.ConversionUtils;
import it.smartcommunitylabdhub.core.models.dtos.ProjectDTO;
import it.smartcommunitylabdhub.core.models.entities.Artifact;
import it.smartcommunitylabdhub.core.models.entities.Function;
import it.smartcommunitylabdhub.core.models.entities.Project;
import it.smartcommunitylabdhub.core.models.entities.Workflow;
import it.smartcommunitylabdhub.core.models.enums.State;

public class ProjectDTOBuilder {

        private Project project;
        private List<Artifact> artifacts;
        private List<Function> functions;
        private List<Workflow> workflows;
        private boolean embeddable;

        public ProjectDTOBuilder(
                        Project project,
                        List<Artifact> artifacts,
                        List<Function> functions,
                        List<Workflow> workflows,
                        boolean embeddable) {
                this.project = project;
                this.functions = functions;
                this.workflows = workflows;
                this.artifacts = artifacts;
                this.embeddable = embeddable;
        }

        public ProjectDTO build() {
                return EntityFactory.create(ProjectDTO::new, project, builder -> {
                        builder
                                        .with(dto -> dto.setId(project.getId()))
                                        .with(dto -> dto.setName(project.getName()))
                                        .with(dto -> dto.setDescription(project.getDescription()))
                                        .with(dto -> dto.setSource(project.getSource()))
                                        .with(dto -> dto.setState(project.getState() == null ? State.CREATED.name()
                                                        : project.getState().name()))
                                        .with(dto -> dto.setExtra(ConversionUtils.reverse(
                                                        project.getExtra(),
                                                        "cbor")))

                                        .with(dto -> dto.setFunctions(
                                                        functions.stream()
                                                                        .map(f -> new FunctionDTOBuilder(
                                                                                        f, embeddable).build())
                                                                        .collect(Collectors.toList())))
                                        .with(dto -> dto.setArtifacts(
                                                        artifacts.stream()
                                                                        .map(a -> new ArtifactDTOBuilder(
                                                                                        a, embeddable).build())
                                                                        .collect(Collectors.toList())))
                                        .with(dto -> dto.setWorkflows(
                                                        workflows.stream()
                                                                        .map(w -> new WorkflowDTOBuilder(
                                                                                        w, embeddable).build())
                                                                        .collect(Collectors.toList())))
                                        .with(dto -> dto.setCreated(project.getCreated()))
                                        .with(dto -> dto.setUpdated(project.getUpdated()));

                });
        }
}