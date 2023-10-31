package it.smartcommunitylabdhub.core.models.entities.project.specs;

import it.smartcommunitylabdhub.core.models.base.BaseSpec;
import lombok.*;

import java.util.ArrayList;
import java.util.List;


@Getter
@Setter
@AllArgsConstructor
@NoArgsConstructor
@Builder
public class ProjectBaseSpec extends BaseSpec {

    String context;

    String source;

    @Builder.Default
    List<Object> functions = new ArrayList<>();

    @Builder.Default
    List<Object> artifacts = new ArrayList<>();

    @Builder.Default
    List<Object> workflows = new ArrayList<>();
    
    @Builder.Default
    List<Object> dataitems = new ArrayList<>();


}
