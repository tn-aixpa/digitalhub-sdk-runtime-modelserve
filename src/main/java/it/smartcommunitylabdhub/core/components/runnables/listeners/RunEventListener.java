package it.smartcommunitylabdhub.core.components.runnables.listeners;

import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.CompletableFuture;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

import it.smartcommunitylabdhub.core.annotations.CoreHanlder;
import it.smartcommunitylabdhub.core.components.runnables.events.RunMessage;
import it.smartcommunitylabdhub.core.components.runnables.interfaces.MessageHandler;
import it.smartcommunitylabdhub.core.components.workflows.PollingService;
import it.smartcommunitylabdhub.core.components.workflows.factory.Workflow;
import it.smartcommunitylabdhub.core.components.workflows.functions.RunWorkflowBuilder;

@Component
@CoreHanlder
public class RunEventListener implements MessageHandler<RunMessage> {

    @Autowired
    private PollingService pollingService;

    @Override
    public CompletableFuture<Void> handle(RunMessage message) {
        return CompletableFuture.runAsync(() -> {
            try {
                List<Workflow> workflows = new ArrayList<>();
                workflows.add(RunWorkflowBuilder.buildWorkflow(message.getRunDTO()));

                pollingService.createPoller("run:" + message.getRunDTO().getId(),
                        workflows, 2, true);

                pollingService.startOne("run:" + message.getRunDTO().getId());

            } catch (Exception e) {
                System.out.println(e.getMessage());
            }
        });
    }
}
