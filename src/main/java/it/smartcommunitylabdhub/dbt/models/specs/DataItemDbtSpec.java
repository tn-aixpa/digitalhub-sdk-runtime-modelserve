package it.smartcommunitylabdhub.dbt.models.specs;

import com.fasterxml.jackson.annotation.JsonProperty;
import it.smartcommunitylabdhub.core.annotations.common.SpecType;
import it.smartcommunitylabdhub.core.components.infrastructure.factories.specs.SpecEntity;
import it.smartcommunitylabdhub.core.models.entities.dataitem.specs.DataItemBaseSpec;
import lombok.Getter;
import lombok.Setter;


@Getter
@Setter
@SpecType(kind = "dbt", entity = SpecEntity.DATAITEM)
public class DataItemDbtSpec extends DataItemBaseSpec<DataItemDbtSpec> {
    @JsonProperty("raw_code")
    private String rawCode;
    @JsonProperty("compiled_code")
    private String compiledCode;

    @Override
    protected void configureSpec(DataItemDbtSpec dataItemDbtSpec) {
        this.setKey(dataItemDbtSpec.getKey());
        this.setPath(dataItemDbtSpec.getPath());
        this.setRawCode(dataItemDbtSpec.getRawCode());
        this.setCompiledCode(dataItemDbtSpec.getCompiledCode());
        this.setExtraSpecs(dataItemDbtSpec.getExtraSpecs());
    }
}
