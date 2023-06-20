package it.smartcommunitylabdhub.core.services;

import java.util.List;
import java.util.stream.Collectors;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.ApplicationEventPublisher;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Service;

import it.smartcommunitylabdhub.core.components.runnables.events.messages.JobMessage;
import it.smartcommunitylabdhub.core.exceptions.CoreException;
import it.smartcommunitylabdhub.core.exceptions.CustomException;
import it.smartcommunitylabdhub.core.models.builders.dtos.RunDTOBuilder;
import it.smartcommunitylabdhub.core.models.builders.entities.RunEntityBuilder;
import it.smartcommunitylabdhub.core.models.builders.runs.RunBuilderFactory;
import it.smartcommunitylabdhub.core.models.dtos.ExtraDTO;
import it.smartcommunitylabdhub.core.models.dtos.RunDTO;
import it.smartcommunitylabdhub.core.models.dtos.TaskDTO;
import it.smartcommunitylabdhub.core.models.entities.Run;
import it.smartcommunitylabdhub.core.repositories.RunRepository;
import it.smartcommunitylabdhub.core.services.interfaces.RunService;

@Service
public class RunSerivceImpl implements RunService {

    @Autowired
    RunDTOBuilder runDTOBuilder;

    private final RunRepository runRepository;
    private final RunBuilderFactory runBuilderFactory;
    private final ApplicationEventPublisher applicationEventPublisher;
    private final RunEntityBuilder runEntityBuilder;

    public RunSerivceImpl(RunRepository runRepository, RunBuilderFactory runBuilderFactory,
            ApplicationEventPublisher applicationEventPublisher, RunEntityBuilder runEntityBuilder) {
        this.runRepository = runRepository;
        this.runBuilderFactory = runBuilderFactory;
        this.applicationEventPublisher = applicationEventPublisher;
        this.runEntityBuilder = runEntityBuilder;
    }

    @Override
    public List<RunDTO> getRuns(Pageable pageable) {
        try {
            Page<Run> runPage = this.runRepository.findAll(pageable);
            return runPage.getContent().stream()
                    .map(run -> runDTOBuilder.build(run))
                    .collect(Collectors.toList());

        } catch (CustomException e) {
            throw new CoreException(
                    "InternalServerError",
                    e.getMessage(),
                    HttpStatus.INTERNAL_SERVER_ERROR);
        }
    }

    @Override
    public RunDTO getRun(String uuid) {
        return runRepository.findById(uuid)
                .map(run -> runDTOBuilder.build(run))
                .orElseThrow(() -> new CoreException(
                        "RunNotFound",
                        "The run you are searching for does not exist.",
                        HttpStatus.NOT_FOUND));
    }

    @Override
    public boolean deleteRun(String uuid) {
        try {
            this.runRepository.deleteById(uuid);
            return true;
        } catch (Exception e) {
            throw new CoreException(
                    "InternalServerError",
                    "cannot delete artifact",
                    HttpStatus.INTERNAL_SERVER_ERROR);
        }
    }

    @Override
    public RunDTO createRun(TaskDTO taskDTO) {
        try {

            RunDTO runDTO = runBuilderFactory.getBuilder("job").build(taskDTO);

            Run run = runRepository.save(runEntityBuilder.build(runDTO));

            return runDTOBuilder.build(run);
        } catch (CustomException e) {
            throw new CoreException(
                    "InternalServerError",
                    e.getMessage(),
                    HttpStatus.INTERNAL_SERVER_ERROR);
        }
    }

    @Override
    public RunDTO executeRun(String uuid, ExtraDTO extraDTO) {

        return this.runRepository.findById(uuid).map(run -> {

            RunDTO runDTO = runDTOBuilder.build(run);

            // 4. produce event with the runDTO object
            JobMessage jobMessage = new JobMessage(runDTO);
            applicationEventPublisher.publishEvent(jobMessage);

            return runDTO;

        }).orElseThrow(() -> new CoreException(
                "RunNotFound",
                "The run you are searching for does not exist.",
                HttpStatus.NOT_FOUND));

    }
}
