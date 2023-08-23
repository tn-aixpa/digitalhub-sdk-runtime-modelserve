package it.smartcommunitylabdhub.core.models.dtos.utils;

import java.util.Map;

@FunctionalInterface
public interface StatusFieldHandler {
	void handleStatusField(String state, Map<String, Object> statusMap);
}
