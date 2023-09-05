package it.smartcommunitylabdhub.core.components.kubernetes;

import it.smartcommunitylabdhub.core.models.accessors.utils.TaskAccessor;
import it.smartcommunitylabdhub.core.models.accessors.utils.TaskUtils;
import it.smartcommunitylabdhub.core.models.dtos.RunDTO;


public abstract class K8sAbstractJobBuilder {

	public TaskAccessor getTaskAccessor(RunDTO runDTO) {
		return TaskUtils.parseTask(runDTO.getTask());
	}

	public String getJobName(RunDTO runDTO) {
		return "job" + "-" + getTaskAccessor(runDTO).getKind() + "-" + runDTO.getId();
	}

	public String getContainerName(RunDTO runDTO) {
		return "container-job-" + getTaskAccessor(runDTO).getKind() + "-" + runDTO.getId();
	}

}
