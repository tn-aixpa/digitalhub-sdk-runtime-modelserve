package it.smartcommunitylabdhub.core.models.dtos;

import java.util.Date;
import java.util.HashMap;
import java.util.Map;

import com.fasterxml.jackson.annotation.JsonAnyGetter;
import com.fasterxml.jackson.annotation.JsonAnySetter;
import com.fasterxml.jackson.annotation.JsonIgnore;

import it.smartcommunitylabdhub.core.annotations.ValidateField;
import it.smartcommunitylabdhub.core.models.dtos.utils.StateHandler;
import it.smartcommunitylabdhub.core.models.dtos.utils.StatusFieldUtility;
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
public class WorkflowDTO implements BaseEntity {

    @ValidateField(allowNull = true, fieldType = "uuid", message = "Invalid UUID4 string")
    private String id;

    @NotNull
    @ValidateField
    private String name;
    private String kind;

    @ValidateField
    private String project;
    private Map<String, Object> spec;

    @Builder.Default
    @JsonIgnore
    private Map<String, Object> extra = new HashMap<>();

    private Date created;
    private Date updated;
    @Builder.Default
    private Boolean embedded = false;

    @JsonIgnore
    private String state;

    @JsonAnyGetter
    public Map<String, Object> getExtra() {
        return StatusFieldUtility.addStatusField(extra, state);

    }

    @JsonAnySetter
    public void setExtra(String key, Object value) {
        extra.put(key, value);
        StatusFieldUtility.updateStatusField(extra, state, new StateHandler());
    }
}
