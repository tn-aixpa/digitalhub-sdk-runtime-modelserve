package it.smartcommunitylabdhub.core.utils;

import java.util.ArrayList;
import java.util.Map;
import java.util.Optional;

public class MapUtils {

	private MapUtils() {
	}

	public static Optional<Map<String, Object>> getNestedFieldValue(Map<String, Object> map, String field) {
		Object value = ((Map<?, ?>) map).get(field);

		if (value instanceof Map) {
			@SuppressWarnings("unchecked")
			Map<String, Object> nestedMap = (Map<String, Object>) value;
			return Optional.of(nestedMap);
		} else {
			return Optional.empty();
		}
	}

	@SuppressWarnings("unchecked")
	public static <T> void computeAndAddElement(Map<String, Object> map, String key, T element) {
		((ArrayList<T>) map.computeIfAbsent(key, k -> new ArrayList<>())).add(element);
	}
}
