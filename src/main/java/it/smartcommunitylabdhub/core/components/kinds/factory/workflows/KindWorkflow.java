/**
 * KindWorkflow.java
 *
 * This functional interface represents a generic workflow for processing instances of a specific kind (type).
 *
 * @param <I> The type of the input data for the workflow.
 * @param <O> The type of the output (processed data) from the workflow.
 */

package it.smartcommunitylabdhub.core.components.kinds.factory.workflows;

@FunctionalInterface
public interface KindWorkflow<I, O> {

    /**
     * Process the input data with the defined workflow.
     *
     * @param input The input data to be processed.
     * @return The processed data of the specified output type.
     */
    O build(I input);
}
