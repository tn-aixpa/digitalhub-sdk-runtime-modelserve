package it.smartcommunitylabdhub.core.models.entities.workflow.specs;


import it.smartcommunitylabdhub.core.annotations.common.SpecType;
import it.smartcommunitylabdhub.core.components.infrastructure.factories.specs.SpecEntity;
import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
@SpecType(kind = "job", entity = SpecEntity.WORKFLOW)
public class WorkflowJobSpec extends WorkflowBaseSpec {
}
