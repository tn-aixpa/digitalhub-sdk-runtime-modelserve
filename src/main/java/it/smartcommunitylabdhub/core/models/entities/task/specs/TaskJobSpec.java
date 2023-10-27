package it.smartcommunitylabdhub.core.models.entities.task.specs;

import lombok.Getter;
import lombok.Setter;

import java.util.List;
import java.util.Map;
import it.smartcommunitylabdhub.core.annotations.common.SpecType;

@Getter
@Setter
@SpecType("job")
public class TaskJobSpec extends TaskSpec {

    List<Map<String, Object>> volumes;
    List<Map<String, Object>> volumeMounts;
    List<Map<String, Object>> env;
    Map<String, Object> resources;
}
