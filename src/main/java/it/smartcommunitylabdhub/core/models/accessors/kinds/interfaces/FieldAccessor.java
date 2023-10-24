package it.smartcommunitylabdhub.core.models.accessors.kinds.interfaces;

import java.util.Map;

import org.springframework.util.Assert;

/**
 * Define base accessor
 */
public interface FieldAccessor<T> {

    /**
     * Return a map of fields
     * 
     * @return {@code Map} of claims
     */
    Map<String, T> getFields();

    /**
     * Returns the claim value as a {@code T} type. The claim value is expected to be of type
     * {@code T}.
     * 
     * @param field the name of the field
     * @return
     */
    default T getField(String field) {
        return !hasField(field) ? null : (T) getFields().get(field);
    }

    /**
     * Check if field exist.
     * 
     * @param field
     * @return {@code true} if the field exists, otherwise {@code false}
     */
    default boolean hasField(String field) {
        Assert.notNull(field, "field cannot be null");
        return getFields().containsKey(field);
    }

    /**
     * Given a map and a field check if field exist.
     * 
     * @param field
     * @param map
     * @return {@code true} if the field exists, otherwise {@code false}
     */
    default boolean mapHasField(Map<String, T> map, String field) {
        Assert.notNull(field, "field cannot be null");
        return map.containsKey(field);
    }
}
