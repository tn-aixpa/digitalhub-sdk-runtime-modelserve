/**
 * KindWorkflowFactory.java
 *
 * This class is a factory for managing and providing KindWorkflows for different kinds (types).
 */

package it.smartcommunitylabdhub.core.components.kinds.factory.workflows;

import java.util.List;
import java.util.Map;
import java.util.function.Function;
import java.util.stream.Collectors;

import it.smartcommunitylabdhub.core.annotations.RunWorkflowComponent;

public class KindWorkflowFactory {
    private final Map<String, KindWorkflow<?, ?>> workflowMap;

    /**
     * Constructor to create the KindWorkflowFactory with a list of KindWorkflows.
     *
     * @param workflows The list of KindWorkflows to be managed by the factory.
     */
    public KindWorkflowFactory(List<KindWorkflow<?, ?>> workflows) {
        workflowMap = workflows.stream().collect(Collectors.toMap(this::getTypeFromAnnotation, Function.identity()));
    }

    /**
     * Get the type string from the @RunWorkflowComponent annotation for a given
     * KindWorkflow.
     *
     * @param workflow The KindWorkflow for which to extract the type string.
     * @return The type string extracted from the @RunWorkflowComponent annotation.
     * @throws IllegalArgumentException If no @RunWorkflowComponent annotation is
     *                                  found for the workflow.
     */
    private String getTypeFromAnnotation(KindWorkflow<?, ?> workflow) {
        Class<?> workflowClass = workflow.getClass();
        if (workflowClass.isAnnotationPresent(RunWorkflowComponent.class)) {
            RunWorkflowComponent annotation = workflowClass.getAnnotation(RunWorkflowComponent.class);
            return annotation.type();
        }
        throw new IllegalArgumentException(
                "No @RunWorkflowComponent annotation found for workflow: " + workflowClass.getName());
    }

    /**
     * Get the KindWorkflow for the given type.
     *
     * @param type The type string representing the specific kind for which to
     *             retrieve the KindWorkflow.
     * @param <I>  The input type of the KindWorkflow.
     * @param <O>  The output type (processed data) of the KindWorkflow.
     * @return The KindWorkflow for the specified type.
     * @throws IllegalArgumentException If no KindWorkflow is found for the given
     *                                  type.
     */
    public <I, O> KindWorkflow<I, O> getWorkflow(String type) {
        @SuppressWarnings("unchecked")
        KindWorkflow<I, O> workflow = (KindWorkflow<I, O>) workflowMap.get(type);
        if (workflow == null) {
            throw new IllegalArgumentException("No workflow found for type: " + type);
        }
        return workflow;
    }
}
