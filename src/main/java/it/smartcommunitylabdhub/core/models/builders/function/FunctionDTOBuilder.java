package it.smartcommunitylabdhub.core.models.builders.function;

import it.smartcommunitylabdhub.core.components.infrastructure.factories.specs.SpecRegistry;
import it.smartcommunitylabdhub.core.models.base.interfaces.Spec;
import it.smartcommunitylabdhub.core.models.builders.EntityFactory;
import it.smartcommunitylabdhub.core.models.converters.ConversionUtils;
import it.smartcommunitylabdhub.core.models.converters.types.MetadataConverter;
import it.smartcommunitylabdhub.core.models.entities.function.Function;
import it.smartcommunitylabdhub.core.models.entities.function.FunctionDTO;
import it.smartcommunitylabdhub.core.models.entities.function.metadata.FunctionMetadata;
import it.smartcommunitylabdhub.core.models.enums.State;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

import java.util.Map;
import java.util.Optional;

@Component
public class FunctionDTOBuilder {

    @Autowired
    SpecRegistry<? extends Spec> specRegistry;

    @Autowired
    MetadataConverter<FunctionMetadata> metadataConverter;


    public FunctionDTO build(
            Function function,
            boolean embeddable) {

        // Retrieve spec
        Map<String, Object> spec = ConversionUtils.reverse(function.getSpec(), "cbor");

        // Find function spec
        Spec functionSpec = specRegistry.createSpec(function.getKind(), spec);

        // Add base spec to the one stored in db
        spec.putAll(functionSpec.toMap());

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
                                                FunctionMetadata.class))
                                .orElseGet(FunctionMetadata::new))))


                .withIfElse(embeddable, (dto, condition) -> Optional
                        .ofNullable(function.getEmbedded())
                        .filter(embedded -> !condition
                                || (condition && embedded))
                        .ifPresent(embedded -> dto
                                .setSpec(spec)))
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
