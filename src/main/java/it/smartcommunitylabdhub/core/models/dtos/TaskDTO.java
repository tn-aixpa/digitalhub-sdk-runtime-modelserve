package it.smartcommunitylabdhub.core.models.dtos;

import java.util.Date;
import java.util.HashMap;
import java.util.Map;

import com.fasterxml.jackson.annotation.JsonAnyGetter;
import com.fasterxml.jackson.annotation.JsonAnySetter;
import com.fasterxml.jackson.annotation.JsonIgnore;

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
public class TaskDTO implements BaseEntity {
    private String id;

    @NotNull
    private String task;

    @NotNull
    private String project;

    @NotNull
    private String kind; // for instance build

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
