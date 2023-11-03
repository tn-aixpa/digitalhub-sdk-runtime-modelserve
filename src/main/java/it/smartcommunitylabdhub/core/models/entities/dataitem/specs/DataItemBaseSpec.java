package it.smartcommunitylabdhub.core.models.entities.dataitem.specs;

import it.smartcommunitylabdhub.core.models.base.specs.BaseSpec;
import lombok.Getter;
import lombok.Setter;


@Getter
@Setter
public abstract class DataItemBaseSpec extends BaseSpec {
    private String key;
    private String path;
}
