package it.smartcommunitylabdhub.core.models.builders.dtos;

import java.util.Optional;

import org.springframework.stereotype.Component;

import it.smartcommunitylabdhub.core.models.builders.EntityFactory;
import it.smartcommunitylabdhub.core.models.converters.ConversionUtils;
import it.smartcommunitylabdhub.core.models.dtos.FunctionDTO;
import it.smartcommunitylabdhub.core.models.entities.Function;
import it.smartcommunitylabdhub.core.models.enums.State;

@Component
public class FunctionDTOBuilder {

        public FunctionDTO build(
                        Function function,
                        boolean embeddable) {
                return EntityFactory.create(FunctionDTO::new, function, builder -> builder
                                .with(dto -> dto.setId(function.getId()))
                                .with(dto -> dto.setKind(function.getKind()))
                                .with(dto -> dto.setProject(function.getProject()))
                                .with(dto -> dto.setName(function.getName()))

                                .withIfElse(embeddable, (dto, condition) -> Optional.ofNullable(function.getEmbedded())
                                                .filter(embedded -> !condition
                                                                || (condition && embedded))
                                                .ifPresent(embedded -> dto
                                                                .setSpec(ConversionUtils.reverse(
                                                                                function.getSpec(),

                                                                                "cbor"))))
                                .withIfElse(embeddable, (dto, condition) -> Optional.ofNullable(function.getEmbedded())
                                                .filter(embedded -> !condition
                                                                || (condition && embedded))
                                                .ifPresent(embedded -> dto
                                                                .setExtra(ConversionUtils.reverse(
                                                                                function.getExtra(),

                                                                                "cbor"))))
                                .withIfElse(embeddable, (dto, condition) -> Optional.ofNullable(function.getEmbedded())
                                                .filter(embedded -> !condition
                                                                || (condition && embedded))
                                                .ifPresent(embedded -> dto
                                                                .setCreated(function.getCreated())))
                                .withIfElse(embeddable, (dto, condition) -> Optional.ofNullable(function.getEmbedded())
                                                .filter(embedded -> !condition
                                                                || (condition && embedded))
                                                .ifPresent(embedded -> dto
                                                                .setUpdated(function.getUpdated())))
                                .withIfElse(embeddable, (dto, condition) -> Optional.ofNullable(function.getEmbedded())
                                                .filter(embedded -> !condition
                                                                || (condition && embedded))
                                                .ifPresent(embedded -> dto
                                                                .setEmbedded(function.getEmbedded())))
                                .withIfElse(embeddable, (dto, condition) ->

                                Optional.ofNullable(function.getEmbedded())
                                                .filter(embedded -> !condition
                                                                || (condition && embedded))
                                                .ifPresent(embedded -> dto
                                                                .setState(function.getState() == null
                                                                                ? State.CREATED.name()
                                                                                : function.getState()
                                                                                                .name()))

                                )

                );
        }
}