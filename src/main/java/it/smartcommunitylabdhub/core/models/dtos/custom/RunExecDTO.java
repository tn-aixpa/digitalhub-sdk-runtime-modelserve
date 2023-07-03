package it.smartcommunitylabdhub.core.models.dtos.custom;

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
    String taskID;
    SpecDTO specDTO;
}
