/**
 * KindPublisher.java
 *
 * This functional interface represents a generic publisher for publishing instances of a specific kind (type).
 *
 * @param <I> The type of the input data to publish.
 * @param <O> The type of the output (published data).
 */

package it.smartcommunitylabdhub.core.components.kinds.factory.publishers;

@FunctionalInterface
public interface KindPublisher<I, O> {

    /**
     * Publish the given input data.
     *
     * @param input The input data to be published.
     * @return The published data of the specified output type.
     */
    O publish(I input);
}
