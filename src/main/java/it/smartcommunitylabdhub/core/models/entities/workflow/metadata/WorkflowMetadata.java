package it.smartcommunitylabdhub.core.models.entities.workflow.metadata;

import it.smartcommunitylabdhub.core.models.base.metadata.BaseMetadata;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

@AllArgsConstructor
@NoArgsConstructor
@Getter
@Setter
public class WorkflowMetadata extends BaseMetadata {
    String name;

    String version;

    String description;

    boolean embedded;
}
