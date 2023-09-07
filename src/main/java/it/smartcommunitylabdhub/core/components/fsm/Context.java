package it.smartcommunitylabdhub.core.components.fsm;

import java.util.*;
import java.util.function.Supplier;

class Context<C> {
	private Optional<C> value;

	public Context(Optional<C> data) {
		this.value = data;
	}

	public Optional<C> getValue() {
		return value;
	}

	public void setValue(Optional<C> data) {
		this.value = data;
	}

	public Context<C> deepCopy() {
		if (value.isEmpty()) {
			return new Context<>(Optional.empty()); // Handle empty Optional
		} else if (value.get() instanceof Integer || value.get() instanceof Double
				|| value.get() instanceof String || value.get() instanceof Boolean) {
			// Handle primitive types and common immutable types
			return new Context<>(value);
		} else if (value.get() instanceof List<?>) {
			// Handle deep copy for List
			List<?> originalList = (List<?>) value.get();
			List<Object> copiedList = new ArrayList<>();

			for (Object element : originalList) {
				copiedList.add(deepCopyObject(element));
			}

			return new Context<>(Optional.of((C) copiedList));
		} else if (value.get() instanceof Map<?, ?>) {
			// Handle deep copy for Map
			Map<?, ?> originalMap = (Map<?, ?>) value.get();
			Map<Object, Object> copiedMap = new HashMap<>();

			for (Map.Entry<?, ?> entry : originalMap.entrySet()) {
				Object keyCopy = deepCopyObject(entry.getKey());
				Object valueCopy = deepCopyObject(entry.getValue());
				copiedMap.put(keyCopy, valueCopy);
			}

			return new Context<>(Optional.of((C) copiedMap));
		} else {
			// Handle other custom object types
			return new Context<>(Optional.of((C) deepCopyObject(value.get())));
		}
	}

	private Object deepCopyObject(Object obj) {
		if (obj == null) {
			return null;
		} else if (obj instanceof Context<?>) {
			@SuppressWarnings("unchecked")
			Context<C> contextObj = (Context<C>) obj;
			return contextObj.deepCopy();
		} else {
			// Handle other objects and custom deep copy logic here
			// For simplicity, assume they have a copy constructor
			try {
				Supplier<Object> supplier = () -> {
					try {
						// Assuming the object has a copy constructor (you may need to modify
						// this)
						return obj.getClass().getConstructor(obj.getClass()).newInstance(obj);
					} catch (Exception e) {
						e.printStackTrace();
						return null;
					}
				};
				return supplier.get();
			} catch (Exception e) {
				e.printStackTrace();
				return null;
			}
		}
	}
}
