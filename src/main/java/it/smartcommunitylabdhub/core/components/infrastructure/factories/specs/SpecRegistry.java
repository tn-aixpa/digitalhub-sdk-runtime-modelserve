package it.smartcommunitylabdhub.core.components.infrastructure.factories.specs;

import it.smartcommunitylabdhub.core.models.base.interfaces.Spec;
import lombok.extern.log4j.Log4j2;
import org.springframework.stereotype.Component;

import java.util.HashMap;
import java.util.Map;

@Component
@Log4j2
public class SpecRegistry<T extends Spec> {
    private final Map<String, Class<? extends Spec>> specTypes = new HashMap<>();

    public void registerSpecTypes(Map<String, Class<? extends Spec>> specTypeMap) {
        specTypes.putAll(specTypeMap);
    }

    @SuppressWarnings("unchecked")
    public <S extends T> S createSpec(String specType, Map<String, Object> data) {
        Class<? extends T> specClass = (Class<? extends T>) specTypes.get(specType);
        if (specClass != null) {
            try {
                S spec = (S) specClass.getDeclaredConstructor().newInstance();
                spec.configure(data);
                return spec;
            } catch (Exception e) {
                log.error(e.getMessage());
            }
        }
        return null;
    }
}
