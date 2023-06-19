package it.smartcommunitylabdhub.core.services;

import java.util.List;
import java.util.stream.Collectors;

import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Service;

import it.smartcommunitylabdhub.core.exceptions.CoreException;
import it.smartcommunitylabdhub.core.exceptions.CustomException;
import it.smartcommunitylabdhub.core.models.builders.dtos.RunDTOBuilder;
import it.smartcommunitylabdhub.core.models.dtos.ExtraDTO;
import it.smartcommunitylabdhub.core.models.dtos.RunDTO;
import it.smartcommunitylabdhub.core.models.dtos.TaskDTO;
import it.smartcommunitylabdhub.core.models.entities.Run;
import it.smartcommunitylabdhub.core.repositories.RunRepository;
import it.smartcommunitylabdhub.core.services.interfaces.RunService;

@Service
public class RunSerivceImpl implements RunService {

    private final RunRepository runRepository;

    public RunSerivceImpl(RunRepository runRepository) {
        this.runRepository = runRepository;
    }

    @Override
    public List<RunDTO> getRuns(Pageable pageable) {
        try {
            Page<Run> runPage = this.runRepository.findAll(pageable);
            return runPage.getContent().stream()
                    .map(run -> new RunDTOBuilder(run).build())
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
                .map(run -> new RunDTOBuilder(run).build())
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
            // Build a run and store it on db

            // final Run run = new RunEntityBuilder(runDTO).build();
            // this.runRepository.save(run);

            // return ConversionUtils.reverse(run, "run");

            return null;
        } catch (CustomException e) {
            throw new CoreException(
                    "InternalServerError",
                    e.getMessage(),
                    HttpStatus.INTERNAL_SERVER_ERROR);
        }
    }

    @Override
    public RunDTO executeRun(String uuid, ExtraDTO extraDTO) {
        // TODO Auto-generated method stub
        throw new UnsupportedOperationException("Unimplemented method 'execute'");
    }

    // // 1. get function get if exist otherwise throw exeception.
    // return
    // functionRepository.findLatestFunctionByProjectAndId(taskDTO.getProject(),
    // uuidOrName)
    // .or(() -> functionRepository.findLatestFunctionByProjectAndName(
    // taskDTO.getProject(), uuidOrName))
    // .map(function -> {

    // // 2. store task and create run object
    // Task task = new TaskEntityBuilder(taskDTO).build();
    // taskRepository.save(task);

    // // 3. produce a run object and store it
    // Run run = new RunEntityBuilder(
    // RunDTO.builder()
    // .type(function.getKind())
    // .taskId(task.getId())
    // .project(function.getProject())
    // .name(taskDTO.getName() + "@task:" + task.getId())
    // .body(Map.of())
    // .build())
    // .build();
    // this.runRepository.save(run);

    // // 4. produce event with the runDTO object
    // RunDTO runDTO = new RunDTOBuilder(run).build();
    // JobMessage jobMessage = new JobMessage(runDTO, new
    // TaskDTOBuilder(task).build());
    // messageDispatcher.dispatch(jobMessage);

    // // 5. return the runDTO object to client
    // return runDTO;

    // }).orElseThrow(() -> new CoreException(
    // "FunctionNotFound",
    // "The function you are searching for does not exist.",
    // HttpStatus.NOT_FOUND));
}
