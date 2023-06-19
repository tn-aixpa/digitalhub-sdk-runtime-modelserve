package it.smartcommunitylabdhub.core.components.runnables.events.listeners;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.event.EventListener;
import org.springframework.scheduling.annotation.Async;
import org.springframework.stereotype.Component;

import it.smartcommunitylabdhub.core.components.runnables.events.messages.JobMessage;
import it.smartcommunitylabdhub.core.components.runnables.events.services.interfaces.JobService;

@Component
public class JobEventListener {

    @Autowired
    private JobService jobService;

    @EventListener
    @Async
    public void handle(JobMessage message) {
        String threadName = Thread.currentThread().getName();
        System.out.println("Job Service receive [" + threadName + "] task@"
                + message.getRunDTO().getTaskId() + ":Job@"
                + message.getRunDTO().getId());

        // Call runnable job service
        jobService.run(message.getRunDTO(), message.getTaskDTO());
    }
}
