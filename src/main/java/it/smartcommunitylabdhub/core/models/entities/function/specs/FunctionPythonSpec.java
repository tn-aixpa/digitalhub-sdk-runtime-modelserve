package it.smartcommunitylabdhub.core.models.entities.function.specs;

import it.smartcommunitylabdhub.core.annotations.common.SpecType;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

import java.util.List;

@Getter
@Setter
@AllArgsConstructor
@NoArgsConstructor
@SpecType("python")
public class FunctionPythonSpec extends FunctionBaseSpec {
    private String source;
    private String handler;
    private String image;
    private String command;
    private List<Object> args;
    private List<Object> requirements;
}
