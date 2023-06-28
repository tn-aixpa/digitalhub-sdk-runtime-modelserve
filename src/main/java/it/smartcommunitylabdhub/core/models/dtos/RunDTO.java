package it.smartcommunitylabdhub.core.models.dtos;

import java.util.Date;
import java.util.Map;

import com.fasterxml.jackson.annotation.JsonAnyGetter;
import com.fasterxml.jackson.annotation.JsonAnySetter;
import com.fasterxml.jackson.annotation.JsonIgnore;
import com.fasterxml.jackson.annotation.JsonProperty;

import it.smartcommunitylabdhub.core.annotations.ValidateField;
import it.smartcommunitylabdhub.core.models.interfaces.BaseEntity;

import java.util.HashMap;

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
public class RunDTO implements BaseEntity {
    @NotNull
    private String id;

    @NotNull
    @ValidateField
    private String project;

    @NotNull
    @ValidateField
    private String name;

    @NotNull
    private String type;

    @JsonProperty("task_id")
    private String taskId;

    @Builder.Default
    private Map<String, Object> spec = new HashMap<>();

    @Builder.Default
    @JsonIgnore
    private Map<String, Object> extra = new HashMap<>();

    private Date created;

    private Date updated;

    private String state;

    @JsonAnyGetter
    public Map<String, Object> getExtra() {
        return extra;
    }

    @JsonAnySetter
    public void setExtra(String key, Object value) {
        extra.put(key, value);
    }
}
