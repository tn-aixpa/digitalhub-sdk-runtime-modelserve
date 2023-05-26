package it.smartcommunitylabdhub.core.components.kubernetes.kaniko;

import com.fasterxml.jackson.annotation.*;

import lombok.Getter;
import lombok.Setter;

import java.util.HashMap;
import java.util.Map;

@Getter
@Setter
public class DockerBuildConfiguration {
    private String baseImage;
    private String entrypointCommand;
    private Map<String, Object> additionalProperties = new HashMap<>();

    @JsonProperty("baseImage")
    public String getBaseImage() {
        return baseImage;
    }

    @JsonProperty("baseImage")
    public void setBaseImage(String baseImage) {
        this.baseImage = baseImage;
    }

    @JsonProperty("entrypointCommand")
    public String getEntrypointCommand() {
        return entrypointCommand;
    }

    @JsonProperty("entrypointCommand")
    public void setEntrypointCommand(String entrypointCommand) {
        this.entrypointCommand = entrypointCommand;
    }

    @JsonAnyGetter
    public Map<String, Object> getAdditionalProperties() {
        return this.additionalProperties;
    }

    @JsonAnySetter
    public void setAdditionalProperty(String name, Object value) {
        this.additionalProperties.put(name, value);
    }
}
