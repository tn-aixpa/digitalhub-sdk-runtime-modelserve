package it.smartcommunitylabdhub.core.components.workflows;

import java.util.ArrayList;
import java.util.List;

import it.smartcommunitylabdhub.core.components.workflows.factory.Poller;
import it.smartcommunitylabdhub.core.components.workflows.factory.Workflow;

public class PollingService {
    private final List<Poller> pollerList;

    public PollingService() {
        this.pollerList = new ArrayList<>();
    }

    public void createPoller(String name, List<Workflow> workflowList, long delay, boolean reschedule) {
        Poller poller = new Poller(name, workflowList, delay, reschedule);
        pollerList.add(poller);
    }

    public void startPolling() {
        for (Poller poller : pollerList) {
            poller.startPolling();
        }
    }

    public void stopPolling() {
        for (Poller poller : pollerList) {
            poller.stopPolling();
        }
    }
}