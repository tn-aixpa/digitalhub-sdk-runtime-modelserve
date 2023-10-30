package it.smartcommunitylabdhub.core.models.entities.dataitem.metadata;

import it.smartcommunitylabdhub.core.models.base.Metadata;
import jakarta.validation.constraints.NotEmpty;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

@AllArgsConstructor
@NoArgsConstructor
@Getter
@Setter
public class DataItemMetadata extends Metadata {
    @NotEmpty
    String name;

    @NotEmpty
    String version;

    @NotEmpty
    String description;

    @NotEmpty
    boolean embedded;
}
