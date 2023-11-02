package it.smartcommunitylabdhub.core.models.builders.function;

import it.smartcommunitylabdhub.core.models.builders.EntityFactory;
import it.smartcommunitylabdhub.core.models.converters.ConversionUtils;
import it.smartcommunitylabdhub.core.models.converters.types.MetadataConverter;
import it.smartcommunitylabdhub.core.models.entities.function.Function;
import it.smartcommunitylabdhub.core.models.entities.function.FunctionDTO;
import it.smartcommunitylabdhub.core.models.entities.function.metadata.FunctionBaseMetadata;
import it.smartcommunitylabdhub.core.models.enums.State;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

import java.util.Optional;

@Component
public class FunctionDTOBuilder {

    @Autowired
    MetadataConverter<FunctionBaseMetadata> metadataConverter;

    public FunctionDTO build(
            Function function,
            boolean embeddable) {

        return EntityFactory.create(FunctionDTO::new, function, builder -> builder
                .with(dto -> dto.setId(function.getId()))
                .with(dto -> dto.setKind(function.getKind()))
                .with(dto -> dto.setProject(function.getProject()))
                .with(dto -> dto.setName(function.getName()))

                .withIfElse(embeddable, (dto, condition) -> Optional
                        .ofNullable(function.getEmbedded())
                        .filter(embedded -> !condition
                                || (condition && embedded))
                        .ifPresent(embedded -> dto.setMetadata(Optional
                                .ofNullable(metadataConverter
                                        .reverseByClass(function
                                                        .getMetadata(),
                                                FunctionBaseMetadata.class))
                                .orElseGet(FunctionBaseMetadata::new))))


                .withIfElse(embeddable, (dto, condition) -> Optional
                        .ofNullable(function.getEmbedded())
                        .filter(embedded -> !condition
                                || (condition && embedded))
                        .ifPresent(embedded -> dto
                                .setSpec(ConversionUtils.reverse(
                                        function.getSpec(), "cbor"))))
                .withIfElse(embeddable, (dto, condition) -> Optional
                        .ofNullable(function.getEmbedded())
                        .filter(embedded -> !condition
                                || (condition && embedded))
                        .ifPresent(embedded -> dto
                                .setExtra(ConversionUtils.reverse(
                                        function.getExtra(),

                                        "cbor"))))
                .withIfElse(embeddable, (dto, condition) -> Optional
                        .ofNullable(function.getEmbedded())
                        .filter(embedded -> !condition
                                || (condition && embedded))
                        .ifPresent(embedded -> dto
                                .setCreated(function.getCreated())))
                .withIfElse(embeddable, (dto, condition) -> Optional
                        .ofNullable(function.getEmbedded())
                        .filter(embedded -> !condition
                                || (condition && embedded))
                        .ifPresent(embedded -> dto
                                .setUpdated(function.getUpdated())))
                .withIfElse(embeddable, (dto, condition) -> Optional
                        .ofNullable(function.getEmbedded())
                        .filter(embedded -> !condition
                                || (condition && embedded))
                        .ifPresent(embedded -> dto
                                .setEmbedded(function
                                        .getEmbedded())))
                .withIfElse(embeddable, (dto, condition) ->

                        Optional.ofNullable(function.getEmbedded())
                                .filter(embedded -> !condition
                                        || (condition && embedded))
                                .ifPresent(embedded -> dto
                                        .setState(function
                                                .getState() == null
                                                ? State.CREATED.name()
                                                : function.getState()
                                                .name()))

                )

        );
    }
}
