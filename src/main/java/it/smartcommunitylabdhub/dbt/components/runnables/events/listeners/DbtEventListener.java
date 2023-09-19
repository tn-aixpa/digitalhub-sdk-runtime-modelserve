package it.smartcommunitylabdhub.dbt.components.runnables.events.listeners;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.context.event.EventListener;
import org.springframework.scheduling.annotation.Async;
import org.springframework.stereotype.Component;

import it.smartcommunitylabdhub.core.components.events.services.interfaces.KindService;
import it.smartcommunitylabdhub.core.services.interfaces.RunService;
import it.smartcommunitylabdhub.dbt.components.runnables.events.messages.DbtMessage;
import lombok.extern.log4j.Log4j2;


/**
 * DbtEventListener.java
 *
 * This class listens for Dbt (Data Build Tool) events and triggers the DbtService to build
 * Kubernetes jobs.
 *
 */
@Component
@Log4j2
public class DbtEventListener {

	@Autowired
	@Qualifier("DbtService")
	KindService<Void> dbtService;

	@Autowired
	RunService runService;

	/**
	 * Event listener method that handles Dbt messages asynchronously.
	 *
	 * @param message The DbtMessage containing information about the task.
	 */
	@EventListener
	@Async
	public void handle(DbtMessage message) {

		String threadName = Thread.currentThread().getName();
		log.info("Dbt Service receive [" + threadName + "] task@"
				+ message.getRunDTO().getTaskId()
				+ ":Dbt@"
				+ message.getRunDTO().getId());

		// call dbt service to build kubernetes job
		dbtService.run(message.getRunDTO());

	}
}
