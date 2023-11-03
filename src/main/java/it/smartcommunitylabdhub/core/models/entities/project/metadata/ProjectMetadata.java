package it.smartcommunitylabdhub.core.models.entities.project.metadata;

import it.smartcommunitylabdhub.core.models.base.metadata.BaseMetadata;
import jakarta.validation.constraints.NotEmpty;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;


@AllArgsConstructor
@NoArgsConstructor
@Getter
@Setter
public class ProjectMetadata extends BaseMetadata {
    @NotEmpty
    String name;
    @NotEmpty
    String description;

}
