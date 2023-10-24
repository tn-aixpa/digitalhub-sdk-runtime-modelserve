package it.smartcommunitylabdhub.core.models.validators.interfaces;

import it.smartcommunitylabdhub.core.models.base.interfaces.BaseEntity;

@FunctionalInterface
public interface BaseValidator {
	<T extends BaseEntity> boolean validate(T dto);
}
