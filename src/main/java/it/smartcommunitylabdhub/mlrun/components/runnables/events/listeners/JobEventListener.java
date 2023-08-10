
package it.smartcommunitylabdhub.mlrun.components.runnables.events.listeners;

import it.smartcommunitylabdhub.core.components.events.messages.RunMessage;
import it.smartcommunitylabdhub.core.components.events.services.interfaces.KindService;
import it.smartcommunitylabdhub.core.exceptions.CoreException;
import it.smartcommunitylabdhub.core.models.dtos.RunDTO;
import it.smartcommunitylabdhub.core.services.interfaces.RunService;
import it.smartcommunitylabdhub.core.utils.MapUtils;
import it.smartcommunitylabdhub.mlrun.components.runnables.events.messages.JobMessage;
import java.util.Map;
import java.util.Optional;
import lombok.extern.log4j.Log4j2;
import org.springframework.context.ApplicationEventPublisher;
import org.springframework.context.event.EventListener;
import org.springframework.scheduling.annotation.Async;
import org.springframework.stereotype.Component;

@Component
@Log4j2
public class JobEventListener {

    private final KindService<Map<String, Object>> jobService;

    private final ApplicationEventPublisher eventPublisher;

    private final RunService runService;

    public JobEventListener(RunService runService, ApplicationEventPublisher eventPublisher,
            KindService<Map<String, Object>> jobService) {
        this.runService = runService;
        this.eventPublisher = eventPublisher;
        this.jobService = jobService;
    }

    @EventListener
    @Async
    public void handle(JobMessage message) {

        String threadName = Thread.currentThread().getName();
        log.info("Job Service receive [" + threadName + "] task@" + message.getRunDTO().getTaskId() + ":Job@"
                + message.getRunDTO().getId());

        try {

            Map<String, Object> body = jobService.run(message.getRunDTO());

            // 3. Check the result and perform actions accordingly
            Optional.ofNullable(body).ifPresentOrElse(
                    response -> handleSuccessfulResponse(response, message.getRunDTO()),
                    () -> handleFailedResponse("NullBody", "No run was found on MLRun"));
        } catch (CoreException e) {
            // Handle the CoreException thrown by jobService.run() method
            // You can log the exception or perform any other necessary actions
            // For example:
            handleFailedResponse(e.getErrorCode(), e.getMessage());
        }
    }

    private void handleSuccessfulResponse(Map<String, Object> response, RunDTO runDTO) {

        Optional<Map<String, Object>> optionalData = MapUtils.getNestedFieldValue(response, "data");

        optionalData.ifPresentOrElse(data -> {
            MapUtils.getNestedFieldValue(data, "metadata").ifPresent(metadata -> {
                runDTO.setExtra("mlrun_run_uid", metadata.get("uid"));
            });

            // MapUtils.getNestedFieldValue(data, "status").ifPresent(status -> {
            // runDTO.setExtra("status", status);
            // });

            // Save RunDTO

            RunDTO savedRunDTO = runService.save(runDTO);

            log.info("Dispatch event to RunMessage");
            eventPublisher.publishEvent(RunMessage.builder().runDTO(savedRunDTO).build());
        }, () -> handleFailedResponse("DataNotPresent", "Data is not present in MLRun Run response."));
    }

    private void handleFailedResponse(String statusCode, String errorMessage) {
        throw new CoreException(statusCode, errorMessage, null);
    }
}
