package it.smartcommunitylabdhub.dbt.components.runnables.events.listeners;

import java.util.Map;
import java.util.Optional;
import java.util.concurrent.TimeUnit;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.event.EventListener;
import org.springframework.scheduling.annotation.Async;
import org.springframework.stereotype.Component;
import com.fasterxml.jackson.databind.ObjectMapper;
import io.fabric8.kubernetes.api.model.Event;
import io.fabric8.kubernetes.client.KubernetesClient;
import io.fabric8.kubernetes.client.Watch;
import io.fabric8.kubernetes.client.Watcher;
import io.fabric8.kubernetes.client.WatcherException;
import it.smartcommunitylabdhub.core.components.fsm.enums.RunEvent;
import it.smartcommunitylabdhub.core.components.fsm.enums.RunState;
import it.smartcommunitylabdhub.core.components.kubernetes.EventPrinter;
import it.smartcommunitylabdhub.core.models.builders.entities.LogEntityBuilder;
import it.smartcommunitylabdhub.core.models.dtos.LogDTO;
import it.smartcommunitylabdhub.core.models.dtos.RunDTO;
import it.smartcommunitylabdhub.core.services.interfaces.LogService;
import it.smartcommunitylabdhub.core.services.interfaces.RunService;
import it.smartcommunitylabdhub.dbt.components.runnables.events.messages.DbtKubernetesMessage;
import lombok.extern.log4j.Log4j2;

@Component
@Log4j2
public class DbtKubernetesListener {

	@Autowired
	KubernetesClient kubernetesClient;

	@Autowired
	LogEntityBuilder logEntityBuilder;

	@Autowired
	LogService logService;

	@Autowired
	RunService runService;

	@EventListener
	@Async
	public void handle(DbtKubernetesMessage message) {
		ObjectMapper objectMapper = new ObjectMapper();
		String threadName = Thread.currentThread().getName();

		log.info("Dbt Kubernetes Listener [" + threadName + "] "
				+ message.getK8sJobName()
				+ "@"
				+ message.getK8sNamespace());


		// Watching for current job events.
		Watch watch = kubernetesClient.v1().events().inAnyNamespace().watch(new Watcher<Event>() {
			@Override
			public void eventReceived(Action action, Event event) {
				try {
					// Extract involved object information from the event
					String involvedObjectUid = event.getInvolvedObject().getUid();
					// String involvedObjectName = event.getInvolvedObject().getName();
					// String involvedObjectKind = event.getInvolvedObject().getKind();

					// if event involved object is equal to the job uuid I created before then
					// log event
					if (message.getK8sUuid().equals(involvedObjectUid)) {
						EventPrinter.printEvent(event);

						String eventJson = objectMapper.writeValueAsString(event);

						logService.createLog(LogDTO.builder()
								.run(message.getRunDTO().getId())
								.project(message.getRunDTO().getProject())
								.body(Map.of("content", eventJson))
								.build());


						if (event.getReason().equals("SuccessfulCreate")) {
							message.getFsm().processEvent(RunEvent.BUILD, Optional.empty());
						}

						// when message is completed update run
						if (event.getReason().equals("Completed")) {
							RunDTO runDTO = runService.getRun(message.getRunDTO().getId());
							runDTO.setState(RunState.COMPLETED.name());
							runService.updateRun(runDTO, runDTO.getId());
						}


					}

				} catch (Exception e) {
					log.error(e.getMessage());
				}

			}


			@Override
			public void onClose(WatcherException cause) {
				if (cause != null) {
					// Handle any KubernetesClientException that occurred during
					// watch
					System.err.println(
							"An error occurred during the Kubernetes events watch: "
									+ cause.getMessage());
				} else {
					// Handle watch closure
					System.out.println(
							"The Kubernetes events watch has been closed.");
				}
			}
		});

		// Waiting Until job is succeded..this is thread blocking functionality for this reason
		// every watcher is on @Async method.
		kubernetesClient.batch().v1().jobs().inNamespace(message.getK8sNamespace())
				.withName(message.getK8sJobName())
				.waitUntilCondition(pod -> pod.getStatus().getSucceeded() != null
						&& pod.getStatus().getSucceeded() > 0, 5L, TimeUnit.MINUTES);

		String jobLogs =
				kubernetesClient.batch().v1().jobs().inNamespace(message.getK8sNamespace())
						.withName(message.getK8sJobName())
						.getLog();



		System.out.println(jobLogs);

		// Close watching job execution
		watch.close();

		// Clean up job
		kubernetesClient.batch().v1().jobs().inNamespace(message.getK8sNamespace())
				.withName(message.getK8sJobName())
				.delete();


	}
}
