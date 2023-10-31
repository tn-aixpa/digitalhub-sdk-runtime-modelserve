package it.smartcommunitylabdhub.core.models.base;


import it.smartcommunitylabdhub.core.annotations.common.SpecType;
import it.smartcommunitylabdhub.core.components.infrastructure.factories.specs.SpecEntity;
import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
@SpecType(kind = "none", entity = SpecEntity.NONE)
public class NoneBaseSpec extends BaseSpec {
}
