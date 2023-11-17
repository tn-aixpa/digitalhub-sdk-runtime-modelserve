package it.smartcommunitylabdhub.core.models.entities;

import lombok.extern.slf4j.Slf4j;

import java.lang.reflect.Field;
import java.util.HashMap;
import java.util.Map;
import java.util.Optional;


@Slf4j
public class StatusFieldUtility {

    StatusFieldUtility() {
    }

    @SuppressWarnings("unchecked")
    public static Map<String, Object> addStatusField(Map<String, Object> extra, String state) {
        Map<String, Object> updatedExtra = new HashMap<>(extra);

        updatedExtra.compute("status", (key, value) -> {
            Map<String, Object> statusMap = Optional.ofNullable((Map<String, Object>) value)
                    .orElse(new HashMap<>());
            statusMap.put("state", state);
            return statusMap;
        });

        return updatedExtra;
    }

    @SuppressWarnings("unchecked")
    public static void updateStateField(Object dto) {
        try {
            // Use reflection to access the 'extra' and 'state' fields of the DTO
            Field extraField = dto.getClass().getDeclaredField("extra");
            extraField.setAccessible(true);

            Field stateField = dto.getClass().getDeclaredField("state");
            stateField.setAccessible(true);

            Map<String, Object> extra = (Map<String, Object>) extraField.get(dto);

            if (extra.containsKey("status")) {
                Map<String, Object> statusMap = (Map<String, Object>) extra.get("status");
                if (statusMap != null && statusMap.containsKey("state")) {
                    Object stateValue = statusMap.get("state");
                    if (stateValue != null) {
                        stateField.set(dto, stateValue.toString().toUpperCase());
                    } else {
                        if (statusMap.isEmpty()) {
                            extra.remove("status");
                        }
                    }
                }
            }

        } catch (NoSuchFieldException | IllegalAccessException e) {
            log.error(e.getMessage());
        }
    }

}
