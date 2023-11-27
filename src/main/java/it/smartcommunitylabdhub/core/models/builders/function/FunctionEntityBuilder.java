package it.smartcommunitylabdhub.core.models.builders.function;

import it.smartcommunitylabdhub.core.components.infrastructure.factories.specs.SpecEntity;
import it.smartcommunitylabdhub.core.components.infrastructure.factories.specs.SpecRegistry;
import it.smartcommunitylabdhub.core.models.base.interfaces.Spec;
import it.smartcommunitylabdhub.core.models.builders.EntityFactory;
import it.smartcommunitylabdhub.core.models.converters.ConversionUtils;
import it.smartcommunitylabdhub.core.models.entities.function.Function;
import it.smartcommunitylabdhub.core.models.entities.function.FunctionDTO;
import it.smartcommunitylabdhub.core.models.entities.function.specs.FunctionBaseSpec;
import it.smartcommunitylabdhub.core.models.enums.State;
import it.smartcommunitylabdhub.core.utils.JacksonMapper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

import java.util.Map;

@Component
public class FunctionEntityBuilder {


    @Autowired
    SpecRegistry<? extends Spec> specRegistry;

    /**
     * Build a function from a functionDTO and store extra values as a cbor
     *
     * @param functionDTO the functionDTO that need to be stored
     * @return Function
     */
    public Function build(FunctionDTO functionDTO) {

        specRegistry.createSpec(functionDTO.getKind(), SpecEntity.FUNCTION, Map.of());

        // Retrieve Spec
        FunctionBaseSpec<?> spec = JacksonMapper.objectMapper
                .convertValue(functionDTO.getSpec(), FunctionBaseSpec.class);

        return EntityFactory.combine(
                ConversionUtils.convert(functionDTO, "function"), functionDTO,
                builder -> builder
                        .with(f -> f.setMetadata(
                                ConversionUtils.convert(functionDTO
                                                .getMetadata(),
                                        "metadata")))
                        .with(f -> f.setExtra(
                                ConversionUtils.convert(functionDTO
                                                .getExtra(),
                                        "cbor")))
                        .with(f -> f.setSpec(
                                ConversionUtils.convert(spec.toMap(),
                                        "cbor"))));
    }

    /**
     * Update a function if element is not passed it override causing empty field
     *
     * @param function the function to update
     * @return Function
     */
    public Function update(Function function, FunctionDTO functionDTO) {

        // Retrieve object spec
        FunctionBaseSpec spec = JacksonMapper.objectMapper
                .convertValue(functionDTO.getSpec(), FunctionBaseSpec.class);

        return EntityFactory.combine(
                function, functionDTO, builder -> builder
                        .with(f -> f.setState(functionDTO.getState() == null
                                ? State.CREATED
                                : State.valueOf(functionDTO
                                .getState())))
                        .with(f -> f.setMetadata(
                                ConversionUtils.convert(functionDTO
                                                .getMetadata(),
                                        "metadata")))

                        .with(f -> f.setExtra(
                                ConversionUtils.convert(functionDTO
                                                .getExtra(),

                                        "cbor")))
                        .with(f -> f.setSpec(
                                ConversionUtils.convert(spec.toMap(),
                                        "cbor")))
                        .with(f -> f.setEmbedded(
                                functionDTO.getEmbedded())));
    }
}
