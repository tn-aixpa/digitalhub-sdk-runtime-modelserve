package it.smartcommunitylabdhub.core.components.infrastructure.runnables;

import java.util.Map;
import it.smartcommunitylabdhub.core.annotations.RunnableComponent;
import it.smartcommunitylabdhub.core.components.infrastructure.factories.runnables.BaseRunnable;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Getter;
import lombok.NoArgsConstructor;


@RunnableComponent(framework = "k8sjob")
@Builder
@Getter
@AllArgsConstructor
@NoArgsConstructor
public class K8sJobRunnable extends BaseRunnable {

	String name;

	String image;

	String command;

	String state;

	String[] args;

	Map<String, String> envs;

	@Override
	public String framework() {
		return "k8sjob";
	}

}
