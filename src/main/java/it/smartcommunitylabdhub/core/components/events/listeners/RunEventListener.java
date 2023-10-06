package it.smartcommunitylabdhub.core.components.events.listeners;

import java.util.ArrayList;
import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.event.EventListener;
import org.springframework.scheduling.annotation.Async;
import org.springframework.stereotype.Component;

import it.smartcommunitylabdhub.core.components.events.messages.RunMessage;
import it.smartcommunitylabdhub.core.components.kinds.factory.workflows.KindWorkflowFactory;
import it.smartcommunitylabdhub.core.components.pollers.PollingService;
import it.smartcommunitylabdhub.core.components.workflows.factory.Workflow;
import it.smartcommunitylabdhub.core.models.accessors.utils.RunAccessor;
import it.smartcommunitylabdhub.core.models.accessors.utils.RunUtils;

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

        RunAccessor runAccessor = RunUtils.parseRun(message.getRunDTO().getTask());

        // This kindWorkflowFactory allow specific workflow generation based on task
        // field type
        workflows.add((Workflow) kindWorkflowFactory
                .getWorkflow(runAccessor.getRuntime(), runAccessor.getTask())
                .build(message.getRunDTO()));

        // Create new run poller
        pollingService.createPoller("run:" + message.getRunDTO().getId(),
                workflows, 2, true);

        // Start poller
        pollingService.startOne("run:" + message.getRunDTO().getId());
    }
}
