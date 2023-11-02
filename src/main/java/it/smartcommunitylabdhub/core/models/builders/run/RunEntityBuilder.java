package it.smartcommunitylabdhub.core.models.builders.run;

import it.smartcommunitylabdhub.core.components.fsm.enums.RunState;
import it.smartcommunitylabdhub.core.models.base.JacksonMapper;
import it.smartcommunitylabdhub.core.models.builders.EntityFactory;
import it.smartcommunitylabdhub.core.models.converters.ConversionUtils;
import it.smartcommunitylabdhub.core.models.entities.run.Run;
import it.smartcommunitylabdhub.core.models.entities.run.RunDTO;
import it.smartcommunitylabdhub.core.models.entities.run.specs.RunBaseSpec;
import org.springframework.stereotype.Component;

@Component
public class RunEntityBuilder extends JacksonMapper {
    
    /**
     * Build a Run from a RunDTO and store extra values as a cbor
     *
     * @param runDTO the run dto
     * @return Run
     */
    public Run build(RunDTO runDTO) {
        // Create run Object
        Run run = ConversionUtils.convert(runDTO, "run");
        // Retrieve base spec
        RunBaseSpec spec = mapper.convertValue(runDTO.getSpec(), RunBaseSpec.class);

        // Merge Task and TaskId
        run.setTask(spec.getTask());
        run.setTaskId(spec.getTaskId());

        return EntityFactory.combine(
                run, runDTO,
                builder -> builder
                        .with(r -> r.setMetadata(
                                ConversionUtils.convert(
                                        runDTO.getMetadata(),
                                        "metadata")))
                        .with(r -> r.setExtra(
                                ConversionUtils.convert(
                                        runDTO.getExtra(),
                                        "cbor")))
                        .with(r -> r.setSpec(
                                ConversionUtils.convert(
                                        spec.toMap(),
                                        "cbor"))));

    }

    /**
     * Update a Run if element is not passed it override causing empty field
     *
     * @param run    the Run
     * @param runDTO the run DTO
     * @return Run
     */
    public Run update(Run run, RunDTO runDTO) {
        // Retrieve base spec
        RunBaseSpec spec = mapper.convertValue(runDTO.getSpec(), RunBaseSpec.class);

        return EntityFactory.combine(
                run, runDTO, builder -> builder
                        .with(r -> r.setKind(runDTO.getKind()))
                        .with(r -> r.setTask(run.getTask()))
                        .with(r -> r.setTaskId(spec.getTaskId()))
                        .with(r -> r.setProject(runDTO.getProject()))
                        .with(r -> r.setState(runDTO.getState() == null
                                ? RunState.CREATED
                                : RunState.valueOf(
                                runDTO.getState())))
                        .with(r -> r.setMetadata(
                                ConversionUtils.convert(
                                        runDTO.getMetadata(),
                                        "metadata")))

                        .with(r -> r.setExtra(
                                ConversionUtils.convert(
                                        runDTO.getExtra(),

                                        "cbor")))
                        .with(r -> r.setSpec(
                                ConversionUtils.convert(
                                        spec.toMap(),
                                        "cbor"))));
    }
}
