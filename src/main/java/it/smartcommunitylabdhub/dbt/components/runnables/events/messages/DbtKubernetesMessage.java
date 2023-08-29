package it.smartcommunitylabdhub.dbt.components.runnables.events.messages;

import java.util.Map;
import it.smartcommunitylabdhub.core.components.events.messages.interfaces.Message;
import it.smartcommunitylabdhub.core.components.fsm.StateMachine;
import it.smartcommunitylabdhub.core.components.fsm.enums.RunEvent;
import it.smartcommunitylabdhub.core.components.fsm.enums.RunState;
import it.smartcommunitylabdhub.core.models.dtos.RunDTO;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

@Getter
@Setter
@AllArgsConstructor
@NoArgsConstructor
@Builder
public class DbtKubernetesMessage implements Message {

	private StateMachine<RunState, RunEvent, Map<String, Object>> fsm;
	private RunDTO runDTO;
	private String k8sJobName;
	private String k8sNamespace;
	private String k8sUuid;
}
