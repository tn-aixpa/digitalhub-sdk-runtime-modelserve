package it.smartcommunitylabdhub.core.models.dtos;

import java.util.Date;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import com.fasterxml.jackson.annotation.JsonAnyGetter;
import com.fasterxml.jackson.annotation.JsonAnySetter;
import com.fasterxml.jackson.annotation.JsonIgnore;

import it.smartcommunitylabdhub.core.annotations.ValidateField;
import it.smartcommunitylabdhub.core.models.interfaces.BaseEntity;
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
public class ProjectDTO implements BaseEntity {
    private String id;

    @NotNull
    @ValidateField
    private String name;
    private String description;
    private String source;

    @Builder.Default
    @JsonIgnore
    private Map<String, Object> extra = new HashMap<>();

    private String state;
    private List<FunctionDTO> functions;
    private List<ArtifactDTO> artifacts;
    private List<WorkflowDTO> workflows;
    private Date created;
    private Date updated;

    @JsonAnyGetter
    public Map<String, Object> getExtra() {
        return extra;
    }

    @JsonAnySetter
    public void setExtra(String key, Object value) {
        extra.put(key, value);
    }

}
