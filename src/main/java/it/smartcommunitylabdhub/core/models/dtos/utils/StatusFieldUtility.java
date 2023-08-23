package it.smartcommunitylabdhub.core.models.dtos.utils;

import java.util.HashMap;
import java.util.Map;
import java.util.Optional;

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
    public static void updateStatusField(Map<String, Object> extra, String state,
            StatusFieldHandler handler) {
        Map<String, Object> updatedExtra = new HashMap<>(extra);

        if (updatedExtra.containsKey("status")) {
            Map<String, Object> statusMap = (Map<String, Object>) updatedExtra.get("status");
            handler.handleStatusField(state, statusMap);
            if (statusMap.isEmpty()) {
                updatedExtra.remove("status");
            }
        }

        // Update the extra map of the DTO
        extra.clear();
        extra.putAll(updatedExtra);
    }
}
