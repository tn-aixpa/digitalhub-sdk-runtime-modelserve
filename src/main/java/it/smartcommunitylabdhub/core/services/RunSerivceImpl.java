package it.smartcommunitylabdhub.core.services;

import java.util.List;
import java.util.Optional;
import java.util.stream.Collectors;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.ApplicationEventPublisher;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Service;

import it.smartcommunitylabdhub.core.components.kinds.factory.builders.KindBuilderFactory;
import it.smartcommunitylabdhub.core.components.kinds.factory.publishers.KindPublisherFactory;
import it.smartcommunitylabdhub.core.exceptions.CoreException;
import it.smartcommunitylabdhub.core.exceptions.CustomException;
import it.smartcommunitylabdhub.core.models.accessors.utils.TaskAccessor;
import it.smartcommunitylabdhub.core.models.accessors.utils.TaskUtils;
import it.smartcommunitylabdhub.core.models.builders.dtos.RunDTOBuilder;
import it.smartcommunitylabdhub.core.models.builders.entities.RunEntityBuilder;
import it.smartcommunitylabdhub.core.models.dtos.RunDTO;
import it.smartcommunitylabdhub.core.models.dtos.custom.RunExecDTO;
import it.smartcommunitylabdhub.core.models.entities.Run;
import it.smartcommunitylabdhub.core.repositories.RunRepository;
import it.smartcommunitylabdhub.core.services.interfaces.RunService;
import it.smartcommunitylabdhub.core.services.interfaces.TaskService;

@Service
public class RunSerivceImpl implements RunService {

    @Autowired
    RunDTOBuilder runDTOBuilder;

    @Autowired
    RunRepository runRepository;

    @Autowired
    TaskService taskService;

    @Autowired
    KindBuilderFactory runBuilderFactory;

    @Autowired
    KindPublisherFactory runPublisherFactory;

    @Autowired
    RunEntityBuilder runEntityBuilder;

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
    public RunDTO save(RunDTO runDTO) {

        return Optional.ofNullable(this.runRepository.save(runEntityBuilder.build(runDTO)))
                .map(run -> runDTOBuilder.build(run))
                .orElseThrow(() -> new CoreException(
                        "RunSaveError",
                        "Problem while saving the run.",
                        HttpStatus.NOT_FOUND));
    }

    @Override
    public RunDTO createRun(RunExecDTO runExecDTO) {

        return Optional.ofNullable(this.taskService.getTask(runExecDTO.getTaskId()))
                .map(taskDTO -> {

                    // parse task to get accessor
                    TaskAccessor taskAccessor = TaskUtils.parseTask(taskDTO.getTask());

                    // build run from task
                    RunDTO runDTO = (RunDTO) runBuilderFactory.getBuilder(taskAccessor.getKind())
                            .build(taskDTO);

                    // if extra field contained override if field in dto is present otherwise put in
                    // extra runDTO
                    runExecDTO.overrideFields(runDTO);

                    // override spec
                    runDTO.getSpec().putAll(runExecDTO.getSpec());

                    // save run
                    Run run = runRepository.save(runEntityBuilder.build(runDTO));

                    // exec run and return run dto
                    return Optional.ofNullable(runDTOBuilder.build(run)).map(
                            r -> {
                                // // Override all spec
                                // r.getSpec().putAll(runExecDTO.getSpec());
                                runPublisherFactory.getPublisher(taskAccessor.getKind()).publish(r);
                                return r;
                            }).orElseThrow(() -> new CoreException(
                                    "",
                                    "",
                                    HttpStatus.INTERNAL_SERVER_ERROR));
                }).orElseThrow(() -> new CoreException(
                        "RunNotFound",
                        "The run you are searching for does not exist.",
                        HttpStatus.NOT_FOUND));

    }
}
