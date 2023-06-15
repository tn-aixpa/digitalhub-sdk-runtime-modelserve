package it.smartcommunitylabdhub.core.components.runnables.listeners;

import java.util.concurrent.CompletableFuture;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

import it.smartcommunitylabdhub.core.annotations.CoreHanlder;
import it.smartcommunitylabdhub.core.components.runnables.events.JobMessage;
import it.smartcommunitylabdhub.core.components.runnables.interfaces.MessageHandler;
import it.smartcommunitylabdhub.core.components.runnables.services.interfaces.JobService;

@Component
@CoreHanlder
public class JobEventListener implements MessageHandler<JobMessage> {

    @Autowired
    private JobService jobService;

    @Override
    public CompletableFuture<Void> handle(JobMessage message) {
        return CompletableFuture.runAsync(() -> {
            try {
                Thread.sleep(3000);
                String threadName = Thread.currentThread().getName();
                System.out.println("Handling JobMessage asynchronously on thread: " + threadName + ", Run ID: "
                        + message.getRunDTO().getId());

                jobService.run(message.getRunDTO());
            } catch (InterruptedException e) {
                System.out.println(e.getMessage());
            }
        });
    }
}
