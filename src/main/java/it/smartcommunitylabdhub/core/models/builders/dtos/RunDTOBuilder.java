package it.smartcommunitylabdhub.core.models.builders.dtos;

import org.springframework.stereotype.Component;

import it.smartcommunitylabdhub.core.models.builders.EntityFactory;
import it.smartcommunitylabdhub.core.models.converters.ConversionUtils;
import it.smartcommunitylabdhub.core.models.dtos.RunDTO;
import it.smartcommunitylabdhub.core.models.entities.Run;
import it.smartcommunitylabdhub.core.models.enums.State;

@Component
public class RunDTOBuilder {

        public RunDTO build(Run run) {
                return EntityFactory.create(RunDTO::new, run, builder -> {
                        builder
                                        .with(dto -> dto.setId(run.getId()))
                                        .with(dto -> dto.setType(run.getType()))
                                        .with(dto -> dto.setTaskId(run.getTaskId()))
                                        .with(dto -> dto.setProject(run.getProject()))
                                        .with(dto -> dto.setName(run.getName()))
                                        .with(dto -> dto.setSpec(ConversionUtils.reverse(run.getSpec(), "cbor")))
                                        .with(dto -> dto.setExtra(ConversionUtils.reverse(run.getExtra(), "cbor")))
                                        .with(dto -> dto.setCreated(run.getCreated()))
                                        .with(dto -> dto.setUpdated(run.getUpdated()))
                                        .with(dto -> dto.setState(run.getState() == null
                                                        ? State.CREATED.name()
                                                        : run.getState()
                                                                        .name()));

                });
        }
}