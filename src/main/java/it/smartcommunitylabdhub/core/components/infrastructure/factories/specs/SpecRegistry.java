package it.smartcommunitylabdhub.core.components.infrastructure.factories.specs;

import it.smartcommunitylabdhub.core.models.base.interfaces.Spec;
import lombok.extern.log4j.Log4j2;
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
    @SuppressWarnings("unchecked")
    public <S extends T> S createSpec(String specType, SpecEntity specEntity, Map<String, Object> data) {
        // Retrieve the class associated with the specified spec type.
        Class<? extends T> specClass = (Class<? extends T>) specTypes.get(specType + "_" + specEntity.name().toLowerCase());

        if (specClass != null) {
            try {
                // Create a new instance of the spec class.
                S spec = (S) specClass.getDeclaredConstructor().newInstance();
                // Configure the spec instance with the provided data.
                spec.configure(data);
                return spec;
            } catch (Exception e) {
                // Handle any exceptions that may occur during instance creation.
                log.error(e.getMessage());
            }
        }

        // If no spec class is found or if an exception occurs, return null.
        return null;
    }
}
