package it.smartcommunitylabdhub.core.models.builders.run;

import it.smartcommunitylabdhub.core.components.infrastructure.factories.specs.SpecEntity;
import it.smartcommunitylabdhub.core.components.infrastructure.factories.specs.SpecRegistry;
import it.smartcommunitylabdhub.core.models.base.interfaces.Spec;
import it.smartcommunitylabdhub.core.models.builders.EntityFactory;
import it.smartcommunitylabdhub.core.models.converters.ConversionUtils;
import it.smartcommunitylabdhub.core.models.converters.types.MetadataConverter;
import it.smartcommunitylabdhub.core.models.entities.run.Run;
import it.smartcommunitylabdhub.core.models.entities.run.RunDTO;
import it.smartcommunitylabdhub.core.models.entities.run.metadata.RunMetadata;
import it.smartcommunitylabdhub.core.models.enums.State;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

import java.util.Map;
import java.util.Optional;

@Component
public class RunDTOBuilder {

    @Autowired
    SpecRegistry<? extends Spec> specRegistry;

    @Autowired
    MetadataConverter<RunMetadata> metadataConverter;

    public RunDTO build(Run run) {

        // Retrieve spec
        Map<String, Object> spec = ConversionUtils.reverse(run.getSpec(), "cbor");

        // Find base run spec
        Spec runSpec = specRegistry.createSpec(
                run.getKind(),
                SpecEntity.RUN,
                spec);

        // Add base spec to the one stored in db
        spec.putAll(runSpec.toMap());

        return EntityFactory.create(RunDTO::new, run, builder -> builder
                .with(dto -> dto.setId(run.getId()))
                .with(dto -> dto.setKind(run.getKind()))
                .with(dto -> dto.setProject(run.getProject()))
                .with(dto -> dto.setMetadata(Optional
                        .ofNullable(metadataConverter.reverseByClass(
                                run.getMetadata(),
                                RunMetadata.class))
                        .orElseGet(RunMetadata::new)

                ))
                .with(dto -> dto.setSpec(spec))
                .with(dto -> dto.setExtra(
                        ConversionUtils.reverse(run.getExtra(), "cbor")))
                .with(dto -> dto.setCreated(run.getCreated()))
                .with(dto -> dto.setUpdated(run.getUpdated()))
                .with(dto -> dto.setState(run.getState() == null
                        ? State.CREATED.name()
                        : run.getState()
                        .name()))

        );
    }
}
