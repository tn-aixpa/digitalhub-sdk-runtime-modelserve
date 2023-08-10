package it.smartcommunitylabdhub.dbt.components.runnables.events.listeners;

import java.util.Map;

import org.springframework.context.ApplicationEventPublisher;
import org.springframework.context.event.EventListener;
import org.springframework.scheduling.annotation.Async;
import org.springframework.stereotype.Component;

import it.smartcommunitylabdhub.core.components.events.services.interfaces.KindService;
import it.smartcommunitylabdhub.core.services.interfaces.RunService;
import it.smartcommunitylabdhub.dbt.components.runnables.events.messages.DbtMessage;
import lombok.extern.log4j.Log4j2;

@Component
@Log4j2
public class DbtEventListener {

	private final KindService<Map<String, Object>> jobService;
	private final ApplicationEventPublisher eventPublisher;
	private final RunService runService;

	public DbtEventListener(RunService runService, ApplicationEventPublisher eventPublisher,
			KindService<Map<String, Object>> jobService) {
		this.runService = runService;
		this.eventPublisher = eventPublisher;
		this.jobService = jobService;
	}

	@EventListener
	@Async
	public void handle(DbtMessage message) {

		String threadName = Thread.currentThread().getName();
		log.info("Dbt Service receive [" + threadName + "] task@" + message.getRunDTO().getTaskId() + ":Dbt@"
				+ message.getRunDTO().getId());
	}
}
