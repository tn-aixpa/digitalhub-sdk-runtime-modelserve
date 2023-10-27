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
import it.smartcommunitylabdhub.core.annotations.olders.RunWorkflowComponent;

public class KindWorkflowFactory {
    private final Map<String, KindWorkflow<?, ?>> workflowMap;

    /**
     * Constructor to create the KindWorkflowFactory with a list of KindWorkflows.
     *
     * @param workflows The list of KindWorkflows to be managed by the factory.
     */
    public KindWorkflowFactory(List<KindWorkflow<?, ?>> workflows) {
        workflowMap = workflows.stream()
                .collect(Collectors.toMap(this::getWorflowNameFromAnnotation, Function.identity()));
    }

    /**
     * Get the platform string from the @RunWorkflowComponent annotation for a given KindWorkflow.
     *
     * @param workflow The KindWorkflow for which to extract the platform string.
     * @return The platform string extracted from the @RunWorkflowComponent annotation.
     * @throws IllegalArgumentException If no @RunWorkflowComponent annotation is found for the
     *         workflow.
     */
    private String getWorflowNameFromAnnotation(KindWorkflow<?, ?> workflow) {
        Class<?> workflowClass = workflow.getClass();
        if (workflowClass.isAnnotationPresent(RunWorkflowComponent.class)) {
            RunWorkflowComponent annotation =
                    workflowClass.getAnnotation(RunWorkflowComponent.class);
            return annotation.platform() + "+" + annotation.perform();
        }
        throw new IllegalArgumentException(
                "No @RunWorkflowComponent annotation found for workflow: "
                        + workflowClass.getName());
    }

    /**
     * Get the KindWorkflow for the given platform.
     *
     * @param platform The platform string representing the specific platform for which to retrieve
     *        the KindWorkflow.
     * @param perform The perform string representing the specific perform action for a given
     *        platform.
     * @param <I> The input platform of the KindWorkflow.
     * @param <O> The output platform (processed data) of the KindWorkflow.
     * @return The KindWorkflow for the specified platform.
     * @throws IllegalArgumentException If no KindWorkflow is found for the given platform.
     */
    public <I, O> KindWorkflow<I, O> getWorkflow(String platform, String perform) {
        @SuppressWarnings("unchecked")
        KindWorkflow<I, O> workflow =
                (KindWorkflow<I, O>) workflowMap.get(platform + "+" + perform);
        if (workflow == null) {
            throw new IllegalArgumentException(
                    "No workflow found for platform: " + platform + "+" + perform);
        }
        return workflow;
    }
}
