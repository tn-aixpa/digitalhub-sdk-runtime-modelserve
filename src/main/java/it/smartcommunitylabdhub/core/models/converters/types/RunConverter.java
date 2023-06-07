package it.smartcommunitylabdhub.core.models.converters.types;

import org.springframework.stereotype.Component;

import it.smartcommunitylabdhub.core.exceptions.CustomException;
import it.smartcommunitylabdhub.core.models.converters.ConversionUtils;
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
                .name(runDTO.getName())
                .type(runDTO.getType())
                .body(ConversionUtils.convert(runDTO.getBody(), "cbor"))
                .state(runDTO.getState() == null ? State.CREATED : State.valueOf(runDTO.getState()))
                .build();
    }

    @Override
    public RunDTO reverseConvert(Run run) throws CustomException {
        return RunDTO.builder()
                .id(run.getId())
                .project(run.getProject())
                .name(run.getName())
                .type(run.getType())
                .body(ConversionUtils.reverse(run.getBody(), "cbor"))
                .state(run.getState() == null ? State.CREATED.name() : run.getState().name())
                .created(run.getCreated())
                .updated(run.getUpdated())
                .build();
    }

}