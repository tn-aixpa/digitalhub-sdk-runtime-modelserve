package it.smartcommunitylabdhub.core.models.entities.function.specs;

import it.smartcommunitylabdhub.core.annotations.common.SpecType;
import it.smartcommunitylabdhub.core.components.infrastructure.factories.specs.SpecEntity;
import it.smartcommunitylabdhub.core.exceptions.CoreException;
import it.smartcommunitylabdhub.core.utils.ErrorList;
import lombok.Getter;
import lombok.Setter;
import org.springframework.http.HttpStatus;

import java.util.List;

@Getter
@Setter
@SpecType(kind = "python", entity = SpecEntity.FUNCTION)
public class FunctionPythonSpec extends FunctionBaseSpec<FunctionPythonSpec> {
    private String source;
    private String handler;
    private String image;
    private String command;
    private List<Object> args;
    private List<Object> requirements;

    @Override
    protected void configureSpec(FunctionPythonSpec functionPythonSpec) {
        super.configureSpec(functionPythonSpec);
        throw new CoreException(
                ErrorList.METHOD_NOT_IMPLEMENTED.getValue(),
                ErrorList.METHOD_NOT_IMPLEMENTED.getReason(),
                HttpStatus.INTERNAL_SERVER_ERROR
        );
    }
}
