package it.smartcommunitylabdhub.core.models.dtos.custom;

import java.lang.reflect.Field;
import java.util.HashMap;
import java.util.Map;

import com.fasterxml.jackson.annotation.JsonAnyGetter;
import com.fasterxml.jackson.annotation.JsonAnySetter;
import com.fasterxml.jackson.annotation.JsonIgnore;
import com.fasterxml.jackson.annotation.JsonProperty;

import it.smartcommunitylabdhub.core.models.dtos.RunDTO;
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
public class ExecutionDTO {
    @NotNull
    @JsonProperty("task_id")
    String taskId;

    @Builder.Default
    private Map<String, Object> spec = new HashMap<>();

    // can pass extra parameter for instance the kind
    @Builder.Default
    @JsonIgnore
    private Map<String, Object> extra = new HashMap<>();

    @JsonAnyGetter
    public Map<String, Object> getExtra() {
        return extra;
    }

    @JsonAnySetter
    public void setExtra(String key, Object value) {
        extra.put(key, value);
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
