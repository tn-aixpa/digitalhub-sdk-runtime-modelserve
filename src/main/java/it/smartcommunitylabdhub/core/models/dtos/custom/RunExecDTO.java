package it.smartcommunitylabdhub.core.models.dtos.custom;

import java.util.HashMap;
import java.util.Map;

import com.fasterxml.jackson.annotation.JsonProperty;

import jakarta.validation.constraints.NotNull;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;
import lombok.ToString;

@AllArgsConstructor
@NoArgsConstructor
@Getter
@Setter
@Builder
@ToString
public class RunExecDTO {
    @NotNull
    @JsonProperty("task_id")
    String taskId;

    @Builder.Default
    private Map<String, Object> spec = new HashMap<>();

}
