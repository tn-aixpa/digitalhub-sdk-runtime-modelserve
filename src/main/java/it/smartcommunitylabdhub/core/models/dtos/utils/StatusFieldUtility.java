package it.smartcommunitylabdhub.core.models.dtos.utils;

import java.util.HashMap;
import java.util.Map;
import java.util.Optional;

public class StatusFieldUtility {
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
}
