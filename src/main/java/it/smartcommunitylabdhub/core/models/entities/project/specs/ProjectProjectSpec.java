package it.smartcommunitylabdhub.core.models.entities.project.specs;

import it.smartcommunitylabdhub.core.annotations.common.SpecType;
import it.smartcommunitylabdhub.core.components.infrastructure.factories.specs.SpecEntity;
import it.smartcommunitylabdhub.core.models.base.specs.BaseSpec;

@SpecType(kind = "project", entity = SpecEntity.PROJECT)
public class ProjectProjectSpec extends ProjectBaseSpec {
    @Override
    protected <S extends T, T extends BaseSpec> void configure(S concreteSpec) {
        ProjectProjectSpec projectProjectSpec = (ProjectProjectSpec) concreteSpec;
        this.setSource(projectProjectSpec.getSource());
        this.setContext(projectProjectSpec.getContext());
        this.setFunctions(projectProjectSpec.getFunctions());
        this.setArtifacts(projectProjectSpec.getArtifacts());
        this.setDataitems(projectProjectSpec.getDataitems());
        this.setWorkflows(projectProjectSpec.getWorkflows());
        this.setExtraSpecs(projectProjectSpec.getExtraSpecs());
    }
}
