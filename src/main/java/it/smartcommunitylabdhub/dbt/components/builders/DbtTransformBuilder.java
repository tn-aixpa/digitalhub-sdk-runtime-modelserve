package it.smartcommunitylabdhub.dbt.components.builders;

import java.util.Map;
import it.smartcommunitylabdhub.core.annotations.infrastructure.BuilderComponent;
import it.smartcommunitylabdhub.core.components.infrastructure.factories.builders.BaseBuilder;
import it.smartcommunitylabdhub.core.components.infrastructure.factories.builders.Builder;
import it.smartcommunitylabdhub.core.models.accessors.utils.RunUtils;
import it.smartcommunitylabdhub.core.models.entities.function.FunctionDTO;
import it.smartcommunitylabdhub.core.models.entities.run.RunDTO;
import it.smartcommunitylabdhub.core.models.entities.task.TaskDTO;
import it.smartcommunitylabdhub.core.utils.MapUtils;

@BuilderComponent(runtime = "dbt", task = "transform")
public class DbtTransformBuilder extends BaseBuilder implements Builder {

	@Override
	public RunDTO build(FunctionDTO functionDTO, TaskDTO taskDTO, RunDTO inputRunDTO) {
		// 1. Merge Task spec with function spec
		Map<String, Object> mergedSpec =
				MapUtils.mergeMaps(functionDTO.getSpec(), taskDTO.getSpec(),
						(oldValue, newValue) -> newValue);

		// 2. produce a run object and store it
		RunDTO runDTO = RunDTO.builder()
				.id(inputRunDTO.getId())
				.kind("run")
				.taskId(taskDTO.getId())
				.project(taskDTO.getProject())
				.task(RunUtils.buildRunString(
						functionDTO,
						taskDTO))
				.spec(mergedSpec)
				.metadata(inputRunDTO.getMetadata())
				.extra(inputRunDTO.getExtra())
				.build();

		// 3. Merge the rest of the spec from executionDTO and the current RunDTO
		return mergeSpec(inputRunDTO, runDTO);

	}



}
