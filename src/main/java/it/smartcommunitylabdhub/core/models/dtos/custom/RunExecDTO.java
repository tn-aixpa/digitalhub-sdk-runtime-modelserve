package it.smartcommunitylabdhub.core.models.dtos.custom;

import com.fasterxml.jackson.annotation.JsonProperty;

import jakarta.validation.constraints.NotNull;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

@AllArgsConstructor
@NoArgsConstructor
@Getter
@Setter
@Builder
public class RunExecDTO {
    @NotNull
    @JsonProperty("task_id")
    String taskId;

    @NotNull
    @Builder.Default
    SpecDTO specDTO = SpecDTO.builder().build();
}
