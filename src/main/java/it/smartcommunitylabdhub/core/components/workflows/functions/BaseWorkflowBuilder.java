package it.smartcommunitylabdhub.core.components.workflows.functions;

import java.util.Map;

import org.springframework.core.ParameterizedTypeReference;
import org.springframework.stereotype.Component;
import org.springframework.web.client.RestTemplate;

@Component
public class BaseWorkflowBuilder {
    protected ParameterizedTypeReference<Map<String, Object>> responseType;
    protected RestTemplate restTemplate;

    public BaseWorkflowBuilder() {
        this.restTemplate = new RestTemplate();
        this.responseType = new ParameterizedTypeReference<Map<String, Object>>() {
        };
    }

}
