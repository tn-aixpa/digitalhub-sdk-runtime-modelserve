package it.smartcommunitylabdhub.core.models.accessors.utils;

import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
public class TaskAccessor {
    private String kind;
    private String project;
    private String function;
    private String version;

    public TaskAccessor(String kind, String project, String function, String version) {
        this.kind = kind;
        this.project = project;
        this.function = function;
        this.version = version;
    }
}
