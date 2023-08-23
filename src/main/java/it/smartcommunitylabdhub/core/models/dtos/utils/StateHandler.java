package it.smartcommunitylabdhub.core.models.dtos.utils;

import java.util.Map;

public class StateHandler implements StatusFieldHandler {
	@Override
	public void handleStatusField(String state, Map<String, Object> statusMap) {
		statusMap.put("state", state);
	}
}
