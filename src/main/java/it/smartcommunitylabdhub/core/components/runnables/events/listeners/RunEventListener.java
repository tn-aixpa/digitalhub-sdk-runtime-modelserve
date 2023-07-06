package it.smartcommunitylabdhub.core.components.runnables.events.listeners;

import java.util.ArrayList;
import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.event.EventListener;
import org.springframework.scheduling.annotation.Async;
import org.springframework.stereotype.Component;

import it.smartcommunitylabdhub.core.components.kinds.factory.workflows.KindWorkflowFactory;
import it.smartcommunitylabdhub.core.components.runnables.events.messages.RunMessage;
import it.smartcommunitylabdhub.core.components.runnables.pollers.PollingService;
import it.smartcommunitylabdhub.core.components.runnables.pollers.workflows.factory.Workflow;

@Component
public class RunEventListener {

    @Autowired
    private PollingService pollingService;

    @Autowired
    KindWorkflowFactory kindWorkflowFactory;

    @EventListener
    @Async
    public void handle(RunMessage message) {

        List<Workflow> workflows = new ArrayList<>();

        // This kindWorkflowFactory allow specific workflow generation based in runDTO
        // kind
        workflows.add((Workflow) kindWorkflowFactory
                .getWorkflow(message.getRunDTO().getKind())
                .build(message.getRunDTO()));

        // Create new run poller
        pollingService.createPoller("run:" + message.getRunDTO().getId(),
                workflows, 2, true);

        // Start poller
        pollingService.startOne("run:" + message.getRunDTO().getId());
    }
}
