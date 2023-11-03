package it.smartcommunitylabdhub.core.components.infrastructure.factories.builders;


import it.smartcommunitylabdhub.core.models.entities.run.RunDTO;
import it.smartcommunitylabdhub.core.utils.MapUtils;

import java.util.Map;

public class BaseBuilder {

    public RunDTO mergeSpec(RunDTO inputRunDTO, RunDTO runDTO) {
        // 1. if extra field contained override if field in dto is present otherwise put in extra runDTO
        inputRunDTO.overrideFields(runDTO);

        // 2. add also Run Spec
        Map<String, Object> mergedSpec = MapUtils.mergeMaps(
                runDTO.getSpec(),
                inputRunDTO.getSpec(), (oldValue, newValue) -> newValue);

        // 3. set spec
        runDTO.setSpec(mergedSpec);

        // 4. return merged runDTO
        return runDTO;
    }

}
