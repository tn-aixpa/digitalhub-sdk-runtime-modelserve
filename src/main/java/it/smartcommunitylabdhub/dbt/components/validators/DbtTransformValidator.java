package it.smartcommunitylabdhub.dbt.components.validators;

import java.io.IOException;
import com.fasterxml.jackson.databind.ObjectMapper;
import it.smartcommunitylabdhub.core.annotations.validators.ValidatorComponent;
import it.smartcommunitylabdhub.core.models.base.interfaces.BaseEntity;
import it.smartcommunitylabdhub.core.models.validators.interfaces.BaseValidator;
import it.smartcommunitylabdhub.core.models.validators.utils.JSONSchemaValidator;
import lombok.extern.log4j.Log4j2;

@Log4j2
@ValidatorComponent(runtime = "dbt", task = "transform")
public class DbtTransformValidator implements BaseValidator {

	@Override
	public <T extends BaseEntity> boolean validate(T dto) {
		try {
			ObjectMapper objectMapper = new ObjectMapper();
			// FIXME:this should be a real schema.
			return JSONSchemaValidator.validateWithSchema(
					objectMapper.writeValueAsString(dto),
					"dbt-transform-schema.json");
		} catch (IOException e) {
			log.error(e.getMessage());
			return false;
		}
	}
}

