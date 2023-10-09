package it.smartcommunitylabdhub.core.components.kubernetes;

import it.smartcommunitylabdhub.core.models.accessors.utils.RunAccessor;
import it.smartcommunitylabdhub.core.models.accessors.utils.RunUtils;
import it.smartcommunitylabdhub.core.models.entities.run.RunDTO;


public abstract class K8sAbstractJobBuilder {

	public RunAccessor getRunAccessor(RunDTO runDTO) {
		return RunUtils.parseRun(runDTO.getTask());
	}

	public String getJobName(RunDTO runDTO) {
		return "job" + "-" + getRunAccessor(runDTO).getRuntime() + "-"
				+ getRunAccessor(runDTO).getTask() + "-" + runDTO.getId();
	}

	public String getContainerName(RunDTO runDTO) {
		return "container-job-" + getRunAccessor(runDTO).getRuntime() + "-"
				+ getRunAccessor(runDTO).getTask() + "-" + runDTO.getId();
	}

}
