package it.smartcommunitylabdhub.core.services.context;

import java.util.List;
import java.util.Optional;
import java.util.stream.Collectors;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Service;

import it.smartcommunitylabdhub.core.exceptions.CoreException;
import it.smartcommunitylabdhub.core.exceptions.CustomException;
import it.smartcommunitylabdhub.core.models.dtos.FunctionDTO;
import it.smartcommunitylabdhub.core.models.entities.Function;
import it.smartcommunitylabdhub.core.repositories.FunctionRepository;
import it.smartcommunitylabdhub.core.models.builders.dtos.FunctionDTOBuilder;
import it.smartcommunitylabdhub.core.models.builders.entities.FunctionEntityBuilder;
import it.smartcommunitylabdhub.core.services.context.interfaces.FunctionContextService;
import jakarta.transaction.Transactional;

@Service
public class FunctionContextServiceImpl extends ContextService implements FunctionContextService {

    @Autowired
    FunctionRepository functionRepository;

    @Override
    public FunctionDTO createFunction(String projectName, FunctionDTO functionDTO) {
        try {
            // Check that project context is the same as the project passed to the
            // functionDTO
            if (!projectName.equals(functionDTO.getProject())) {
                throw new CustomException("Project Context and Function Project does not match", null);
            }

            // Check project context
            checkContext(functionDTO.getProject());

            // Check if function already exist if exist throw exception otherwise create a
            // new one
            Function function = (Function) Optional.ofNullable(functionDTO.getId())
                    .flatMap(id -> functionRepository.findById(id)
                            .map(a -> {
                                throw new CustomException(
                                        "The project already contains an function with the specified UUID.", null);
                            }))
                    .orElseGet(() -> {
                        // Build an function and store it in the database
                        Function newFunction = new FunctionEntityBuilder(functionDTO).build();
                        return functionRepository.save(newFunction);
                    });

            // Return function DTO
            return new FunctionDTOBuilder(

                    function, false).build();

        } catch (CustomException e) {
            throw new CoreException(
                    "InternalServerError",
                    e.getMessage(),
                    HttpStatus.INTERNAL_SERVER_ERROR);
        }
    }

    @Override
    public List<FunctionDTO> getLatestByProjectName(String projectName, Pageable pageable) {
        try {
            checkContext(projectName);

            Page<Function> functionPage = this.functionRepository
                    .findAllLatestFunctionsByProject(projectName,
                            pageable);
            return functionPage.getContent()
                    .stream()
                    .map((function) -> {
                        return new FunctionDTOBuilder(function, false).build();
                    }).collect(Collectors.toList());
        } catch (CustomException e) {
            throw new CoreException(
                    "InternalServerError",
                    e.getMessage(),
                    HttpStatus.INTERNAL_SERVER_ERROR);
        }
    }

    @Override
    public List<FunctionDTO> getByProjectNameAndFunctionName(String projectName, String functionName,
            Pageable pageable) {
        try {
            checkContext(projectName);

            Page<Function> functionPage = this.functionRepository
                    .findAllByProjectAndNameOrderByCreatedDesc(projectName, functionName,
                            pageable);
            return functionPage.getContent()
                    .stream()
                    .map((function) -> {
                        return new FunctionDTOBuilder(function, false).build();
                    }).collect(Collectors.toList());
        } catch (CustomException e) {
            throw new CoreException(
                    "InternalServerError",
                    e.getMessage(),
                    HttpStatus.INTERNAL_SERVER_ERROR);
        }

    }

    @Override
    public FunctionDTO getByProjectAndFunctionAndUuid(String projectName, String functionName,
            String uuid) {
        try {
            // Check project context
            checkContext(projectName);

            return this.functionRepository.findByProjectAndNameAndId(projectName, functionName, uuid).map(
                    function -> new FunctionDTOBuilder(function, false).build())
                    .orElseThrow(
                            () -> new CustomException("The function does not exist.", null));

        } catch (CustomException e) {
            throw new CoreException(
                    "InternalServerError",
                    e.getMessage(),
                    HttpStatus.INTERNAL_SERVER_ERROR);
        }
    }

    @Override
    public FunctionDTO getLatestByProjectNameAndFunctionName(String projectName, String functionName) {
        try {
            // Check project context
            checkContext(projectName);

            return this.functionRepository.findLatestFunctionByProjectAndName(projectName, functionName).map(
                    function -> new FunctionDTOBuilder(function, false).build())
                    .orElseThrow(
                            () -> new CustomException("The function does not exist.", null));

        } catch (CustomException e) {
            throw new CoreException(
                    "InternalServerError",
                    e.getMessage(),
                    HttpStatus.INTERNAL_SERVER_ERROR);
        }
    }

    @Override
    public FunctionDTO createOrUpdateFunction(String projectName, String functionName, FunctionDTO functionDTO) {
        try {
            // Check that project context is the same as the project passed to the
            // functionDTO
            if (!projectName.equals(functionDTO.getProject())) {
                throw new CustomException("Project Context and Function Project does not match.", null);
            }
            if (!functionName.equals(functionDTO.getName())) {
                throw new CustomException(
                        "Trying to create/update an function with name different from the one passed in the request.",
                        null);
            }

            // Check project context
            checkContext(functionDTO.getProject());

            // Check if function already exist if exist throw exception otherwise create a
            // new one
            Function function = Optional.ofNullable(functionDTO.getId())
                    .flatMap(id -> {
                        Optional<Function> optionalFunction = functionRepository.findById(id);
                        if (optionalFunction.isPresent()) {
                            Function existingFunction = optionalFunction.get();

                            // Update the existing function version
                            FunctionEntityBuilder functionBuilder = new FunctionEntityBuilder(
                                    functionDTO);
                            final Function functionUpdated = functionBuilder.update(existingFunction);
                            return Optional.of(this.functionRepository.save(functionUpdated));

                        } else {
                            // Build a new function and store it in the database
                            Function newFunction = new FunctionEntityBuilder(functionDTO).build();
                            return Optional.of(functionRepository.save(newFunction));
                        }
                    })
                    .orElseGet(() -> {
                        // Build a new function and store it in the database
                        Function newFunction = new FunctionEntityBuilder(functionDTO).build();
                        return functionRepository.save(newFunction);
                    });

            // Return function DTO
            return new FunctionDTOBuilder(

                    function, false).build();

        } catch (CustomException e) {
            throw new CoreException(
                    "InternalServerError",
                    e.getMessage(),
                    HttpStatus.INTERNAL_SERVER_ERROR);
        }
    }

    @Override
    public FunctionDTO updateFunction(String projectName, String functionName, String uuid, FunctionDTO functionDTO) {

        try {
            // Check that project context is the same as the project passed to the
            // functionDTO
            if (!projectName.equals(functionDTO.getProject())) {
                throw new CustomException("Project Context and Function Project does not match", null);
            }
            if (!uuid.equals(functionDTO.getId())) {
                throw new CustomException(
                        "Trying to update an function with an ID different from the one passed in the request.", null);
            }
            // Check project context
            checkContext(functionDTO.getProject());

            Function function = this.functionRepository.findById(functionDTO.getId()).map(
                    a -> {
                        // Update the existing function version
                        FunctionEntityBuilder functionBuilder = new FunctionEntityBuilder(
                                functionDTO);
                        return functionBuilder.update(a);
                    })
                    .orElseThrow(
                            () -> new CustomException("The function does not exist.", null));

            // Return function DTO
            return new FunctionDTOBuilder(

                    function, false).build();

        } catch (CustomException e) {
            throw new CoreException(
                    "InternalServerError",
                    e.getMessage(),
                    HttpStatus.INTERNAL_SERVER_ERROR);
        }
    }

    @Override
    @Transactional
    public Boolean deleteSpecificFunctionVersion(String projectName, String functionName, String uuid) {
        try {
            if (this.functionRepository.existsByProjectAndNameAndId(projectName, functionName, uuid)) {
                this.functionRepository.deleteByProjectAndNameAndId(projectName, functionName, uuid);
                return true;
            }
            throw new CoreException(
                    "FunctionNotFound",
                    "The function you are trying to delete does not exist.",
                    HttpStatus.NOT_FOUND);
        } catch (Exception e) {
            throw new CoreException(
                    "InternalServerError",
                    "cannot delete function",
                    HttpStatus.INTERNAL_SERVER_ERROR);
        }
    }

    @Override
    @Transactional
    public Boolean deleteAllFunctionVersions(String projectName, String functionName) {
        try {
            if (functionRepository.existsByProjectAndName(projectName, functionName)) {
                this.functionRepository.deleteByProjectAndName(projectName, functionName);
                return true;
            }
            throw new CoreException(
                    "FunctionNotFound",
                    "The functions you are trying to delete does not exist.",
                    HttpStatus.NOT_FOUND);
        } catch (Exception e) {
            throw new CoreException(
                    "InternalServerError",
                    "cannot delete function",
                    HttpStatus.INTERNAL_SERVER_ERROR);
        }
    }
}
