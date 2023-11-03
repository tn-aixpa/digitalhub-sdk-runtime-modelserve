package it.smartcommunitylabdhub.core.models.entities.project.specs;

import it.smartcommunitylabdhub.core.models.base.specs.BaseSpec;
import lombok.Getter;
import lombok.Setter;

import java.util.ArrayList;
import java.util.List;


@Getter
@Setter
public abstract class ProjectBaseSpec extends BaseSpec {

    String context;

    String source;

    List<Object> functions = new ArrayList<>();

    List<Object> artifacts = new ArrayList<>();

    List<Object> workflows = new ArrayList<>();

    List<Object> dataitems = new ArrayList<>();


}
