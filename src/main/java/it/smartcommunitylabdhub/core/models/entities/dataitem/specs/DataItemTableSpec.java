package it.smartcommunitylabdhub.core.models.entities.dataitem.specs;


import it.smartcommunitylabdhub.core.annotations.common.SpecType;
import it.smartcommunitylabdhub.core.components.infrastructure.factories.specs.SpecEntity;
import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
@SpecType(kind = "table", entity = SpecEntity.DATAITEM)
public class DataItemTableSpec extends DataItemBaseSpec {
}
