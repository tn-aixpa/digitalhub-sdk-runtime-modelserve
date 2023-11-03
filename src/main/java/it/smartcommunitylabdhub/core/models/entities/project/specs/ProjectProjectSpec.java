package it.smartcommunitylabdhub.core.models.entities.project.specs;

import it.smartcommunitylabdhub.core.annotations.common.SpecType;
import it.smartcommunitylabdhub.core.components.infrastructure.factories.specs.SpecEntity;

@SpecType(kind = "project", entity = SpecEntity.PROJECT)
public class ProjectProjectSpec extends ProjectBaseSpec<ProjectProjectSpec> {
    @Override
    protected void configureSpec(ProjectProjectSpec projectProjectSpec) {
        super.configureSpec(projectProjectSpec);
        
        this.setSource(projectProjectSpec.getSource());
        this.setContext(projectProjectSpec.getContext());
        this.setFunctions(projectProjectSpec.getFunctions());
        this.setArtifacts(projectProjectSpec.getArtifacts());
        this.setDataitems(projectProjectSpec.getDataitems());
        this.setWorkflows(projectProjectSpec.getWorkflows());
        this.setExtraSpecs(projectProjectSpec.getExtraSpecs());
    }
}
