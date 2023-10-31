package it.smartcommunitylabdhub.core.models.entities.dataitem.specs;

import it.smartcommunitylabdhub.core.models.base.BaseSpec;
import lombok.*;

@AllArgsConstructor
@NoArgsConstructor
@Getter
@Setter
@Builder
public class DataItemBaseSpec extends BaseSpec {
    private String key;
    private String path;
}
