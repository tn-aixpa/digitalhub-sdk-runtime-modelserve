package it.smartcommunitylabdhub.core.models.entities.function.specs;

import it.smartcommunitylabdhub.core.annotations.common.SpecType;
import it.smartcommunitylabdhub.core.components.infrastructure.factories.specs.SpecEntity;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

import java.util.List;

@Getter
@Setter
@AllArgsConstructor
@NoArgsConstructor
@SpecType(kind = "python", entity = SpecEntity.FUNCTION)
public class FunctionPythonSpec extends FunctionBaseSpec {
    private String source;
    private String handler;
    private String image;
    private String command;
    private List<Object> args;
    private List<Object> requirements;
}
