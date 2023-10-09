package it.smartcommunitylabdhub.core.models.entities.run;

import java.lang.reflect.Field;
import java.util.Date;
import java.util.Map;

import com.fasterxml.jackson.annotation.JsonAnyGetter;
import com.fasterxml.jackson.annotation.JsonAnySetter;
import com.fasterxml.jackson.annotation.JsonIgnore;
import com.fasterxml.jackson.annotation.JsonProperty;
import it.smartcommunitylabdhub.core.annotations.ValidateField;
import it.smartcommunitylabdhub.core.models.entities.StatusFieldUtility;
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

    @ValidateField(allowNull = true, fieldType = "uuid", message = "Invalid UUID4 string")
    private String id;

    private String task;

    private String project;

    private String kind;

    @NotNull
    @JsonProperty("task_id")
    private String taskId;

    @Builder.Default
    private Map<String, Object> spec = new HashMap<>();

    @Builder.Default
    @JsonIgnore
    private Map<String, Object> extra = new HashMap<>();

    private Date created;

    private Date updated;

    @JsonIgnore
    private String state;

    @JsonAnyGetter
    public Map<String, Object> getExtra() {
        return StatusFieldUtility.addStatusField(extra, state);
    }

    @JsonAnySetter
    public void setExtra(String key, Object value) {
        if (value != null) {
            extra.put(key, value);
            StatusFieldUtility.updateStateField(this);
        }
    }

    public void overrideFields(RunDTO runDTO) {
        Class<?> runClass = runDTO.getClass();

        for (Map.Entry<String, Object> entry : extra.entrySet()) {
            String fieldName = entry.getKey();
            Object value = entry.getValue();

            try {
                Field field = runClass.getDeclaredField(fieldName);
                field.setAccessible(true);
                field.set(runDTO, value);
            } catch (NoSuchFieldException | IllegalAccessException e) {
                // put field in extra
                runDTO.getExtra().put(fieldName, value);
            }
        }
    }
}
