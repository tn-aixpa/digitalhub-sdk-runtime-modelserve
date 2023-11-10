package it.smartcommunitylabdhub.modules.dbt.components.validators;

import com.fasterxml.jackson.databind.ObjectMapper;
import it.smartcommunitylabdhub.core.annotations.validators.ValidatorComponent;
import it.smartcommunitylabdhub.core.models.base.interfaces.Spec;
import it.smartcommunitylabdhub.core.models.base.metadata.BaseMetadata;
import it.smartcommunitylabdhub.core.models.validators.interfaces.BaseValidator;
import it.smartcommunitylabdhub.core.models.validators.utils.JSONSchemaValidator;
import lombok.extern.log4j.Log4j2;

import java.io.IOException;

@Log4j2
@ValidatorComponent(runtime = "dbt", task = "transform")
public class DbtTransformValidator implements BaseValidator {

    @Override
    public <T extends Spec> boolean validateSpec(T spec) {
        try {
            ObjectMapper objectMapper = new ObjectMapper();
            // FIXME:this should be a real schema.
            return JSONSchemaValidator.validateWithSchema(
                    objectMapper.writeValueAsString(spec),
                    "dbt-transform-schema.json");
        } catch (IOException e) {
            log.error(e.getMessage());
            return false;
        }
    }

    @Override
    public <T extends BaseMetadata> boolean validateMetadata(T metadata) {
        // TODO Auto-generated method stub
        throw new UnsupportedOperationException("Unimplemented method 'validateMetadata'");
    }
}

