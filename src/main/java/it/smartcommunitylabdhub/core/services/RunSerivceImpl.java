package it.smartcommunitylabdhub.core.services;

import it.smartcommunitylabdhub.core.components.infrastructure.factories.runnables.Runnable;
import it.smartcommunitylabdhub.core.components.infrastructure.factories.runtimes.Runtime;
import it.smartcommunitylabdhub.core.components.infrastructure.factories.runtimes.RuntimeFactory;
import it.smartcommunitylabdhub.core.components.kinds.factory.builders.KindBuilderFactory;
import it.smartcommunitylabdhub.core.components.kinds.factory.publishers.KindPublisherFactory;
import it.smartcommunitylabdhub.core.exceptions.CoreException;
import it.smartcommunitylabdhub.core.exceptions.CustomException;
import it.smartcommunitylabdhub.core.models.accessors.utils.TaskAccessor;
import it.smartcommunitylabdhub.core.models.accessors.utils.TaskUtils;
import it.smartcommunitylabdhub.core.models.builders.dtos.RunDTOBuilder;
import it.smartcommunitylabdhub.core.models.builders.entities.RunEntityBuilder;
import it.smartcommunitylabdhub.core.models.entities.run.Run;
import it.smartcommunitylabdhub.core.models.entities.run.RunDTO;
import it.smartcommunitylabdhub.core.repositories.RunRepository;
import it.smartcommunitylabdhub.core.services.interfaces.FunctionService;
import it.smartcommunitylabdhub.core.services.interfaces.RunService;
import it.smartcommunitylabdhub.core.services.interfaces.TaskService;
import it.smartcommunitylabdhub.core.utils.ErrorList;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.ApplicationEventPublisher;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Optional;
import java.util.function.Supplier;
import java.util.stream.Collectors;

@Service
public class RunSerivceImpl implements RunService {

    @Autowired
    RunDTOBuilder runDTOBuilder;

    @Autowired
    RunRepository runRepository;

    @Autowired
    TaskService taskService;

    @Autowired
    FunctionService functionService;

    @Autowired
    RuntimeFactory runtimeFactory;

    @Autowired
    KindBuilderFactory runBuilderFactory;

    @Autowired
    KindPublisherFactory runPublisherFactory;

    @Autowired
    RunEntityBuilder runEntityBuilder;

    @Autowired
    ApplicationEventPublisher eventPublisher;

    @Override
    public List<RunDTO> getRuns(Pageable pageable) {
        try {
            Page<Run> runPage = this.runRepository.findAll(pageable);
            return runPage.getContent().stream().map(run -> runDTOBuilder.build(run))
                    .collect(Collectors.toList());

        } catch (CustomException e) {
            throw new CoreException(ErrorList.INTERNAL_SERVER_ERROR.getValue(),
                    e.getMessage(),
                    HttpStatus.INTERNAL_SERVER_ERROR);
        }
    }

    @Override
    public RunDTO getRun(String uuid) {
        return runRepository.findById(uuid).map(run -> runDTOBuilder.build(run))
                .orElseThrow(() -> new CoreException(
                        ErrorList.RUN_NOT_FOUND.getValue(),
                        ErrorList.RUN_NOT_FOUND.getReason(),
                        HttpStatus.NOT_FOUND));
    }

    @Override
    public boolean deleteRun(String uuid) {
        try {
            this.runRepository.deleteById(uuid);
            return true;
        } catch (Exception e) {
            throw new CoreException(ErrorList.INTERNAL_SERVER_ERROR.getValue(),
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
    public RunDTO updateRun(RunDTO runDTO, String uuid) {

        if (!runDTO.getId().equals(uuid)) {
            throw new CoreException(
                    ErrorList.RUN_NOT_MATCH.getValue(),
                    ErrorList.RUN_NOT_MATCH.getReason(),
                    HttpStatus.NOT_FOUND);
        }

        final Run run = runRepository.findById(uuid).orElse(null);
        if (run == null) {
            throw new CoreException(
                    ErrorList.RUN_NOT_FOUND.getValue(),
                    ErrorList.RUN_NOT_FOUND.getReason(),
                    HttpStatus.NOT_FOUND);
        }

        try {
            final Run runUpdated = runEntityBuilder.update(run, runDTO);
            this.runRepository.save(runUpdated);

            return runDTOBuilder.build(runUpdated);

        } catch (CustomException e) {
            throw new CoreException(
                    ErrorList.INTERNAL_SERVER_ERROR.getValue(),
                    e.getMessage(),
                    HttpStatus.INTERNAL_SERVER_ERROR);
        }
    }

    @Override
    public RunDTO createRun(RunDTO inputRunDTO) {

        if (runRepository.existsById(Optional.ofNullable(inputRunDTO.getId()).orElse(""))) {
            throw new CoreException(ErrorList.DUPLICATE_RUN.getValue(),
                    ErrorList.DUPLICATE_RUN.getReason(),
                    HttpStatus.INTERNAL_SERVER_ERROR);
        }

        return Optional.ofNullable(this.taskService.getTask(inputRunDTO.getTaskId()))
                .map(taskDTO -> {
                    // Parse task to get accessor
                    TaskAccessor taskAccessor =
                            TaskUtils.parseTask(taskDTO.getFunction());

                    return Optional
                            .ofNullable(functionService.getFunction(
                                    taskAccessor.getVersion()))
                            .map(functionDTO -> {

                                // 1. retrieve Runtime and build run
                                Runtime runtime = runtimeFactory
                                        .getRuntime(taskAccessor
                                                .getRuntime());


                                // 2. create Builder
                                // 3. build Run
                                RunDTO buildRunDTO = runtime.build(
                                        functionDTO,
                                        taskDTO,
                                        inputRunDTO);

                                // 4. Save run
                                Run run = runRepository.save(
                                        runEntityBuilder.build(
                                                buildRunDTO));

                                // Check weather the run has local set to True in that case return
                                // immediately the run without invoke the execution.
                                Supplier<RunDTO> result =
                                        () -> Optional
                                                .ofNullable(buildRunDTO
                                                        .getSpec()
                                                        .get("local_execution")) // return
                                                // if true
                                                .filter(value -> value
                                                        .equals(true))

                                                .map(value -> runDTOBuilder
                                                        .build(run))

                                                // exec run and return run dto
                                                .orElseGet(() -> Optional
                                                        .ofNullable(runDTOBuilder
                                                                .build(run))
                                                        .map(savedRun -> {

                                                            // Create Runnable
                                                            Runnable runnable =
                                                                    runtime.run(savedRun);

                                                            // Dispatch  Runnable
                                                            eventPublisher.publishEvent(
                                                                    runnable);

                                                            // Return saved run
                                                            return savedRun;
                                                        })
                                                        .orElseThrow(() -> new CoreException(
                                                                ErrorList.INTERNAL_SERVER_ERROR
                                                                        .getValue(),
                                                                ErrorList.INTERNAL_SERVER_ERROR
                                                                        .getReason(),
                                                                HttpStatus.INTERNAL_SERVER_ERROR)));

                                return result.get();
                            }).orElseThrow(
                                    () -> new CoreException(
                                            ErrorList.FUNCTION_NOT_FOUND
                                                    .getValue(),
                                            ErrorList.FUNCTION_NOT_FOUND
                                                    .getReason(),
                                            HttpStatus.NOT_FOUND));


                })
                .orElseThrow(() -> new CoreException(
                        ErrorList.RUN_NOT_FOUND.getValue(),
                        ErrorList.RUN_NOT_FOUND.getReason(),
                        HttpStatus.NOT_FOUND));

    }

}
