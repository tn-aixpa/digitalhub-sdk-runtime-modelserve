package it.smartcommunitylabdhub.core.services;

import it.smartcommunitylabdhub.core.exceptions.CoreException;
import it.smartcommunitylabdhub.core.exceptions.CustomException;
import it.smartcommunitylabdhub.core.models.accessors.utils.RunUtils;
import it.smartcommunitylabdhub.core.models.accessors.utils.TaskUtils;
import it.smartcommunitylabdhub.core.models.builders.dtos.FunctionDTOBuilder;
import it.smartcommunitylabdhub.core.models.builders.dtos.TaskDTOBuilder;
import it.smartcommunitylabdhub.core.models.builders.entities.FunctionEntityBuilder;
import it.smartcommunitylabdhub.core.models.converters.ConversionUtils;
import it.smartcommunitylabdhub.core.models.entities.function.Function;
import it.smartcommunitylabdhub.core.models.entities.function.FunctionDTO;
import it.smartcommunitylabdhub.core.models.entities.run.Run;
import it.smartcommunitylabdhub.core.models.entities.run.RunDTO;
import it.smartcommunitylabdhub.core.repositories.FunctionRepository;
import it.smartcommunitylabdhub.core.repositories.RunRepository;
import it.smartcommunitylabdhub.core.repositories.TaskRepository;
import it.smartcommunitylabdhub.core.services.interfaces.FunctionService;
import it.smartcommunitylabdhub.core.utils.ErrorList;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Optional;
import java.util.stream.Collectors;

@Service
public class FunctionServiceImpl implements FunctionService {

    @Autowired
    FunctionRepository functionRepository;

    @Autowired
    RunRepository runRepository;

    @Autowired
    TaskRepository taskRepository;

    @Autowired
    FunctionDTOBuilder functionDTOBuilder;

    @Autowired
    FunctionEntityBuilder functionEntityBuilder;

    @Autowired
    TaskDTOBuilder taskDTOBuilder;

    @Override
    public List<FunctionDTO> getFunctions(Pageable pageable) {
        try {
            Page<Function> functionPage = this.functionRepository.findAll(pageable);
            return functionPage.getContent().stream()
                    .map(function -> functionDTOBuilder.build(function, false))
                    .collect(Collectors.toList());
        } catch (CustomException e) {
            throw new CoreException(
                    ErrorList.INTERNAL_SERVER_ERROR.getValue(),
                    e.getMessage(),
                    HttpStatus.INTERNAL_SERVER_ERROR);
        }

    }

    @Override
    public List<FunctionDTO> getFunctions() {
        try {
            List<Function> functions = this.functionRepository.findAll();
            return functions.stream().map(function -> functionDTOBuilder.build(function, false))
                    .collect(Collectors.toList());
        } catch (CustomException e) {
            throw new CoreException(
                    ErrorList.FUNCTION_NOT_FOUND.getValue(),
                    e.getMessage(),
                    HttpStatus.INTERNAL_SERVER_ERROR);
        }
    }

    @Override
    public FunctionDTO createFunction(FunctionDTO functionDTO) {
        if (functionDTO.getId() != null && functionRepository.existsById(functionDTO.getId())) {
            throw new CoreException(
                    ErrorList.DUPLICATE_FUNCTION.getValue(),
                    ErrorList.DUPLICATE_FUNCTION.getReason(),
                    HttpStatus.INTERNAL_SERVER_ERROR);
        }
        Optional<Function> savedFunction = Optional.ofNullable(functionDTO)
                .map(functionEntityBuilder::build)
                .map(this.functionRepository::save);

        return savedFunction.map(function -> functionDTOBuilder.build(function, false))
                .orElseThrow(() -> new CoreException(
                        ErrorList.INTERNAL_SERVER_ERROR.getValue(),
                        "Error saving function",
                        HttpStatus.INTERNAL_SERVER_ERROR));
    }

    @Override
    public FunctionDTO getFunction(String uuid) {

        final Function function = functionRepository.findById(uuid).orElse(null);
        if (function == null) {
            throw new CoreException(
                    ErrorList.FUNCTION_NOT_FOUND.getValue(),
                    ErrorList.FUNCTION_NOT_FOUND.getReason(),
                    HttpStatus.NOT_FOUND);
        }

        try {
            return functionDTOBuilder.build(function, false);

        } catch (CustomException e) {
            throw new CoreException(
                    ErrorList.INTERNAL_SERVER_ERROR.getValue(),
                    e.getMessage(),
                    HttpStatus.INTERNAL_SERVER_ERROR);
        }
    }

    @Override
    public FunctionDTO updateFunction(FunctionDTO functionDTO, String uuid) {

        if (!functionDTO.getId().equals(uuid)) {
            throw new CoreException(
                    ErrorList.FUNCTION_NOT_MATCH.getValue(),
                    ErrorList.FUNCTION_NOT_MATCH.getReason(),
                    HttpStatus.NOT_FOUND);
        }

        final Function function = functionRepository.findById(uuid).orElse(null);
        if (function == null) {
            throw new CoreException(
                    ErrorList.FUNCTION_NOT_FOUND.getValue(),
                    ErrorList.FUNCTION_NOT_FOUND.getReason(),
                    HttpStatus.NOT_FOUND);
        }

        try {

            final Function functionUpdated = functionEntityBuilder.update(function, functionDTO);
            this.functionRepository.save(functionUpdated);

            return functionDTOBuilder.build(functionUpdated, false);

        } catch (CustomException e) {
            throw new CoreException(
                    ErrorList.INTERNAL_SERVER_ERROR.getValue(),
                    e.getMessage(),
                    HttpStatus.INTERNAL_SERVER_ERROR);
        }
    }

    @Override
    public boolean deleteFunction(String uuid) {
        try {
            if (this.functionRepository.existsById(uuid)) {
                this.functionRepository.deleteById(uuid);
                return true;
            }
            throw new CoreException(
                    ErrorList.FUNCTION_NOT_FOUND.getValue(),
                    ErrorList.FUNCTION_NOT_FOUND.getReason(),
                    HttpStatus.NOT_FOUND);
        } catch (Exception e) {
            throw new CoreException(
                    ErrorList.INTERNAL_SERVER_ERROR.getValue(),
                    "Cannot delete function",
                    HttpStatus.INTERNAL_SERVER_ERROR);
        }
    }

    @Override
    public List<RunDTO> getFunctionRuns(String uuid) {
        final Function function = functionRepository.findById(uuid).orElse(null);
        if (function == null) {
            throw new CoreException(
                    ErrorList.FUNCTION_NOT_FOUND.getValue(),
                    ErrorList.FUNCTION_NOT_FOUND.getReason(),
                    HttpStatus.NOT_FOUND);
        }

        FunctionDTO functionDTO = functionDTOBuilder.build(function, false);
        try {
            // Find and collect runs for a function
            List<Run> runs =
                    this.taskRepository.findByFunction(TaskUtils.buildTaskString(functionDTO))
                            .stream()
                            .flatMap(task -> this.runRepository
                                    .findByTask(
                                            RunUtils.buildRunString(
                                                    functionDTO,
                                                    taskDTOBuilder.build(task)))
                                    .stream())
                            .collect(Collectors.toList());


            return (List<RunDTO>) ConversionUtils.reverseIterable(runs, "run", RunDTO.class);

        } catch (CustomException e) {
            throw new CoreException(
                    ErrorList.FUNCTION_NOT_FOUND.getValue(),
                    e.getMessage(),
                    HttpStatus.INTERNAL_SERVER_ERROR);
        }
    }

    @Override
    public List<FunctionDTO> getAllLatestFunctions() {
        try {

            List<Function> functionList = this.functionRepository.findAllLatestFunctions();
            return functionList
                    .stream()
                    .map(function -> functionDTOBuilder.build(function, false))
                    .collect(Collectors.toList());
        } catch (CustomException e) {
            throw new CoreException(
                    ErrorList.FUNCTION_NOT_FOUND.getValue(),
                    e.getMessage(),
                    HttpStatus.INTERNAL_SERVER_ERROR);
        }
    }
}
