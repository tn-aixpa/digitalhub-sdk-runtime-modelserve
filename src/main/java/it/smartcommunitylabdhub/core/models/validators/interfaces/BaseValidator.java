package it.smartcommunitylabdhub.core.models.validators.interfaces;

import it.smartcommunitylabdhub.core.models.base.Metadata;
import it.smartcommunitylabdhub.core.models.base.Spec;


public interface BaseValidator {
	<T extends Spec> boolean validateSpec(T spec);

	<T extends Metadata> boolean validateMetadata(T metadata);
}
