package it.smartcommunitylabdhub.mlrun.config;

import java.util.ArrayList;
import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Configuration;

import it.smartcommunitylabdhub.core.components.runnables.pollers.PollingService;
import it.smartcommunitylabdhub.core.components.runnables.pollers.workflows.factory.Workflow;
import it.smartcommunitylabdhub.mlrun.components.pollers.functions.FunctionWorkflowBuilder;
import jakarta.annotation.PostConstruct;

@Configuration
public class PollerConfig {

    @Autowired
    private PollingService pollingService;

    @Autowired
    FunctionWorkflowBuilder functionWorkflowBuilder;

    @PostConstruct
    public void initialize() {

        // Create and configure Function Workflow
        List<Workflow> coreMlrunSyncWorkflow = new ArrayList<>();
        coreMlrunSyncWorkflow.add(functionWorkflowBuilder.build());

        // Create a new poller and start it.
        pollingService.createPoller("DHCore-Mlrun-Sync", coreMlrunSyncWorkflow, 5, true);
        pollingService.startOne("DHCore-Mlrun-Sync");
    }

}
