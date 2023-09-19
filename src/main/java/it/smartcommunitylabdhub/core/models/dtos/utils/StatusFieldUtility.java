package it.smartcommunitylabdhub.core.models.dtos.utils;

import java.lang.reflect.Field;
import java.util.HashMap;
import java.util.Map;
import java.util.Optional;
import lombok.extern.log4j.Log4j2;



@Log4j2
public class StatusFieldUtility {

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
                if (statusMap.containsKey("state")) {
                    stateField.set(dto, statusMap.get("state").toString().toUpperCase());
                } else {
                    if (statusMap.isEmpty()) {
                        extra.remove("status");
                    }
                }
            }

        } catch (NoSuchFieldException | IllegalAccessException e) {
            log.error(e.getMessage());
        }
    }

}
