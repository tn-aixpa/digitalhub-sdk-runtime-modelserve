package it.smartcommunitylabdhub.core.components.infrastructure.factories.specs;

import it.smartcommunitylabdhub.core.annotations.common.SpecType;
import it.smartcommunitylabdhub.core.models.base.interfaces.Spec;
import jakarta.annotation.PostConstruct;
import org.springframework.context.ApplicationContext;
import org.springframework.stereotype.Component;

import java.util.HashMap;
import java.util.Map;

/**
 * The `SpecTypeFactory` class is responsible for scanning the classpath to discover
 * classes annotated with `@SpecType`. It extracts the information from these classes and
 * registers them in the `SpecRegistry` for later instantiation.
 */

@Component
public class SpecTypeFactory {
    private final SpecRegistry<?> specRegistry;

    private final ApplicationContext applicationContext;

    /**
     * Constructor to inject the `SpecRegistry` instance.
     *
     * @param specRegistry The `SpecRegistry` used to register discovered spec types.
     */
    public SpecTypeFactory(SpecRegistry<?> specRegistry, ApplicationContext applicationContext) {
        this.specRegistry = specRegistry;
        this.applicationContext = applicationContext;
    }


    /**
     * This method is annotated with `@PostConstruct`, ensuring it's executed after bean
     * instantiation. It scans the classpath to discover classes annotated with `@SpecType`,
     * extracts the relevant information, and registers them in the `SpecRegistry`.
     */
    @PostConstruct
    @SuppressWarnings("unchecked")
    public void scanForSpecTypes() {

        Map<String, Class<? extends Spec>> specTypes = new HashMap<>();

        // Use autowiring to get all beans annotated with @SpecType
        Map<String, Object> beansWithAnnotation = applicationContext.getBeansWithAnnotation(SpecType.class);

        for (Object bean : beansWithAnnotation.values()) {
            Class<? extends Spec> specClass = (Class<? extends Spec>) bean.getClass();
            SpecType specTypeAnnotation = specClass.getAnnotation(SpecType.class);
            String specKey = specTypeAnnotation.kind() + "_" + specTypeAnnotation.entity().name().toLowerCase();
            if (!specTypeAnnotation.runtime().isEmpty()) {
                specKey = specTypeAnnotation.runtime() + "_" + specKey;
            }
            specTypes.put(specKey, specClass);
        }

        specRegistry.registerSpecTypes(specTypes);
    }
}
