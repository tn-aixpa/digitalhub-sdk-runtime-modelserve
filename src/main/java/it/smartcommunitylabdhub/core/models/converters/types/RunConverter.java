package it.smartcommunitylabdhub.core.models.converters.types;

import org.springframework.stereotype.Component;

import it.smartcommunitylabdhub.core.exceptions.CustomException;
import it.smartcommunitylabdhub.core.models.converters.interfaces.Converter;
import it.smartcommunitylabdhub.core.models.dtos.RunDTO;
import it.smartcommunitylabdhub.core.models.entities.Run;
import it.smartcommunitylabdhub.core.models.enums.State;

@Component
public class RunConverter implements Converter<RunDTO, Run> {

    @Override
    public Run convert(RunDTO runDTO) throws CustomException {
        return Run.builder()
                .id(runDTO.getId())
                .project(runDTO.getProject())
                .task(runDTO.getTask())
                .kind(runDTO.getKind())
                .taskId(runDTO.getTaskId())
                .state(runDTO.getState() == null ? State.CREATED : State.valueOf(runDTO.getState()))
                .build();
    }

    @Override
    public RunDTO reverseConvert(Run run) throws CustomException {
        return RunDTO.builder()
                .id(run.getId())
                .project(run.getProject())
                .task(run.getTask())
                .kind(run.getKind())
                .taskId(run.getTaskId())
                .state(run.getState() == null ? State.CREATED.name() : run.getState().name())
                .created(run.getCreated())
                .updated(run.getUpdated())
                .build();
    }

}