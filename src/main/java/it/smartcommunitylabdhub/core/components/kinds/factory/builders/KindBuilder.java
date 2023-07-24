/**
 * KindBuilder.java
 *
 * This functional interface represents a generic builder for creating instances of a specific kind (type).
 *
 * @param <I> The type of the input used to build the kind.
 * @param <O> The type of the output (kind) built by the builder.
 */

package it.smartcommunitylabdhub.core.components.kinds.factory.builders;

@FunctionalInterface
public interface KindBuilder<I, O> {

    /**
     * Build an instance of the specific kind using the provided input.
     *
     * @param input The input data to build the kind.
     * @return The built instance of the kind (output).
     */
    O build(I input);
}
