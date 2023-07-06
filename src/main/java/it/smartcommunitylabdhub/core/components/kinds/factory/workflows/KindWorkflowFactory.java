package it.smartcommunitylabdhub.core.components.kinds.factory.workflows;

import java.util.List;
import java.util.Map;
import java.util.function.Function;
import java.util.stream.Collectors;

import it.smartcommunitylabdhub.core.annotations.RunWorkflowComponent;

public class KindWorkflowFactory {
    private final Map<String, KindWorkflow<?, ?>> workflowMap;

    public KindWorkflowFactory(List<KindWorkflow<?, ?>> workflows) {
        workflowMap = workflows.stream()
                .collect(Collectors.toMap(this::getTypeFromAnnotation, Function.identity()));
    }

    private String getTypeFromAnnotation(KindWorkflow<?, ?> workflow) {
        Class<?> workflowClass = workflow.getClass();
        if (workflowClass.isAnnotationPresent(RunWorkflowComponent.class)) {
            RunWorkflowComponent annotation = workflowClass.getAnnotation(RunWorkflowComponent.class);
            return annotation.type();
        }
        throw new IllegalArgumentException(
                "No @RunWorkflowComponent annotation found for workflow: " + workflowClass.getName());
    }

    public <I, O> KindWorkflow<I, O> getWorkflow(String type) {
        @SuppressWarnings("unchecked")
        KindWorkflow<I, O> workflow = (KindWorkflow<I, O>) workflowMap.get(type);
        if (workflow == null) {
            throw new IllegalArgumentException("No workflow found for type: " + type);
        }
        return workflow;
    }
}
