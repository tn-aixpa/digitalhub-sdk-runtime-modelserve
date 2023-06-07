package it.smartcommunitylabdhub.core.services.builders.dtos;

import java.util.List;
import java.util.stream.Collectors;

import it.smartcommunitylabdhub.core.models.converters.CommandFactory;
import it.smartcommunitylabdhub.core.models.converters.ConversionUtils;
import it.smartcommunitylabdhub.core.models.dtos.ProjectDTO;
import it.smartcommunitylabdhub.core.models.entities.Artifact;
import it.smartcommunitylabdhub.core.models.entities.Function;
import it.smartcommunitylabdhub.core.models.entities.Project;
import it.smartcommunitylabdhub.core.models.entities.Workflow;
import it.smartcommunitylabdhub.core.models.enums.State;
import it.smartcommunitylabdhub.core.services.factory.EntityFactory;

public class ProjectDTOBuilder {

        private CommandFactory commandFactory;
        private Project project;
        private List<Artifact> artifacts;
        private List<Function> functions;
        private List<Workflow> workflows;
        private boolean embeddable;

        public ProjectDTOBuilder(
                        CommandFactory commandFactory,
                        Project project,
                        List<Artifact> artifacts,
                        List<Function> functions,
                        List<Workflow> workflows,
                        boolean embeddable) {
                this.project = project;
                this.commandFactory = commandFactory;
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
                                                        commandFactory,
                                                        "cbor")))

                                        .with(dto -> dto.setFunctions(
                                                        functions.stream()
                                                                        .map(f -> new FunctionDTOBuilder(commandFactory,
                                                                                        f, embeddable).build())
                                                                        .collect(Collectors.toList())))
                                        .with(dto -> dto.setArtifacts(
                                                        artifacts.stream()
                                                                        .map(a -> new ArtifactDTOBuilder(commandFactory,
                                                                                        a, embeddable).build())
                                                                        .collect(Collectors.toList())))
                                        .with(dto -> dto.setWorkflows(
                                                        workflows.stream()
                                                                        .map(w -> new WorkflowDTOBuilder(commandFactory,
                                                                                        w, embeddable).build())
                                                                        .collect(Collectors.toList())))
                                        .with(dto -> dto.setCreated(project.getCreated()))
                                        .with(dto -> dto.setUpdated(project.getUpdated()));

                });
        }
}