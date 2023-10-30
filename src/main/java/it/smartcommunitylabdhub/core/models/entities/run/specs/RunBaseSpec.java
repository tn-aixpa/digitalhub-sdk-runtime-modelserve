package it.smartcommunitylabdhub.core.models.entities.run.specs;

import com.fasterxml.jackson.annotation.JsonAnyGetter;
import com.fasterxml.jackson.annotation.JsonAnySetter;
import com.fasterxml.jackson.annotation.JsonProperty;
import it.smartcommunitylabdhub.core.models.base.BaseSpec;
import jakarta.validation.constraints.NotEmpty;
import lombok.*;

import java.util.HashMap;
import java.util.Map;

@AllArgsConstructor
@NoArgsConstructor
@Getter
@Setter
@Builder
public class RunBaseSpec extends BaseSpec {

    @NotEmpty
    private String task;

    @NotEmpty
    @JsonProperty("task_id")
    private String taskId;

    @Builder.Default
    private Map<String, Object> inputs = new HashMap<>();

    @Builder.Default
    private Map<String, Object> outputs = new HashMap<>();

    @Builder.Default
    private Map<String, Object> parameters = new HashMap<>();

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
