package it.smartcommunitylabdhub.core.models.entities.run;

import com.fasterxml.jackson.annotation.JsonAnyGetter;
import com.fasterxml.jackson.annotation.JsonAnySetter;
import com.fasterxml.jackson.annotation.JsonProperty;
import jakarta.validation.constraints.NotEmpty;
import lombok.*;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

@AllArgsConstructor
@NoArgsConstructor
@Getter
@Setter
@Builder
public class RunSpec {

    @NotEmpty
    private String task;

    @NotEmpty
    @JsonProperty("task_id")
    private String taskId;

    private List<Object> inputs;

    private List<Object> outputs;

    private List<Object> parameters;

    @Builder.Default
    @JsonProperty("local_execution")
    private boolean localExecution = false;

    @Builder.Default
    private Map<String, Object> spec = new HashMap<>();

    @JsonAnyGetter
    public Map<String, Object> getSpec() {
        return spec;
    }

    @JsonAnySetter
    public void setSpec(String key, Object value) {
        if (value != null) {
            spec.put(key, value);
        }
    }
}
