package it.smartcommunitylabdhub.core.components.infrastructure.factories.specs;

import it.smartcommunitylabdhub.core.exceptions.CoreException;
import it.smartcommunitylabdhub.core.models.base.interfaces.Spec;
import it.smartcommunitylabdhub.core.utils.ErrorList;
import lombok.extern.log4j.Log4j2;
import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Component;

import java.util.HashMap;
import java.util.Map;

@Component
@Log4j2
public class SpecRegistry<T extends Spec> {
    // A map to store spec types and their corresponding classes.
    private final Map<String, Class<? extends Spec>> specTypes = new HashMap<>();

    // Register spec types along with their corresponding classes.
    public void registerSpecTypes(Map<String, Class<? extends Spec>> specTypeMap) {
        specTypes.putAll(specTypeMap);
    }

    /**
     * Create an instance of a spec based on its type and configure it with data.
     *
     * @param specType The type of the spec to create.
     * @param data     The data used to configure the spec.
     * @param <S>      The generic type for the spec.
     * @return An instance of the specified spec type, or null if not found or in case of errors.
     */
    public <S extends T> S createSpec(String specType, SpecEntity specEntity, Map<String, Object> data) {
        // Retrieve the class associated with the specified spec type.
        final String specKey = specType + "_" + specEntity.name().toLowerCase();
        return getSpec(data, specKey);
    }

    public <S extends T> S createSpec(String specRuntime, String specType, SpecEntity specEntity, Map<String, Object> data) {
        // Retrieve the class associated with the specified spec type.
        final String specKey = specRuntime + "_" + specType + "_" + specEntity.name().toLowerCase();
        return getSpec(data, specKey);
    }


    @SuppressWarnings("unchecked")
    public <S extends T> S getSpec(Map<String, Object> data, String specKey) {
        Class<? extends T> specClass = (Class<? extends T>) specTypes.get(specKey);

        if (specClass == null) {
            // Fallback spec None if no class specific is found, avoid crash.
            specClass = (Class<? extends T>) specTypes.get("none_none");
        }

        try {
            // Create a new instance of the spec class.
            S spec = (S) specClass.getDeclaredConstructor().newInstance();
            // Configure the spec instance with the provided data.
            spec.configure(data);
            return spec;
        } catch (Exception e) {
            // Handle any exceptions that may occur during instance creation.
            log.error("Cannot configure spec for type @SpecType('" + specKey + "') no way to recover error.");
            throw new CoreException(ErrorList.INTERNAL_SERVER_ERROR.getValue(),
                    "Cannot configure spec for type @SpecType('" + specKey + "')", HttpStatus.INTERNAL_SERVER_ERROR);

        }
    }
}
