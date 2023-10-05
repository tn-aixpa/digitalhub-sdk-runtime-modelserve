package it.smartcommunitylabdhub.core.components.infrastructure.factories.runners;

import it.smartcommunitylabdhub.core.components.infrastructure.factories.frameworks.Framework;
import it.smartcommunitylabdhub.core.models.dtos.RunDTO;


/**
 * Prender il RunDTO e produce il Runnable
 */
public interface Runner extends Framework {
	<O> O produce(RunDTO runDTO);
}
