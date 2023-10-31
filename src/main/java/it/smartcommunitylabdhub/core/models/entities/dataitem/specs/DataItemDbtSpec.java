package it.smartcommunitylabdhub.core.models.entities.dataitem.specs;

import com.fasterxml.jackson.annotation.JsonProperty;
import it.smartcommunitylabdhub.core.annotations.common.SpecType;
import it.smartcommunitylabdhub.core.components.infrastructure.factories.specs.SpecEntity;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;


@Getter
@Setter
@AllArgsConstructor
@NoArgsConstructor
@SpecType(kind = "dbt", entity = SpecEntity.DATAITEM)
public class DataItemDbtSpec extends DataItemBaseSpec {
    @JsonProperty("raw_code")
    private String rawCode;

    @JsonProperty("compiled_code")
    private String compiledCode;
}
