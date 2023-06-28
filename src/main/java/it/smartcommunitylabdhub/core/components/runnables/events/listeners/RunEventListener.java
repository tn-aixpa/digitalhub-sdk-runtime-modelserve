package it.smartcommunitylabdhub.core.components.runnables.events.listeners;

import java.util.ArrayList;
import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.event.EventListener;
import org.springframework.scheduling.annotation.Async;
import org.springframework.stereotype.Component;

import it.smartcommunitylabdhub.core.components.runnables.events.messages.RunMessage;
import it.smartcommunitylabdhub.core.components.runnables.pollers.PollingService;
import it.smartcommunitylabdhub.core.components.runnables.pollers.workflows.factory.Workflow;
import it.smartcommunitylabdhub.core.components.runnables.pollers.workflows.functions.RunWorkflowBuilder;

@Component
public class RunEventListener {

    @Autowired
    private PollingService pollingService;

    @Autowired
    RunWorkflowBuilder runWorkflowBuilder;

    @EventListener
    @Async
    public void handle(RunMessage message) {

        // Build workflow
        List<Workflow> workflows = new ArrayList<>();
        workflows.add(runWorkflowBuilder.buildWorkflow(message.getRunDTO()));

        pollingService.createPoller("run:" + message.getRunDTO().getId(),
                workflows, 2, true);

        pollingService.startOne("run:" + message.getRunDTO().getId());
    }
}
