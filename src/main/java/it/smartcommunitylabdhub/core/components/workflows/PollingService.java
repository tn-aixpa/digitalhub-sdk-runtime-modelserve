package it.smartcommunitylabdhub.core.components.workflows;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

import it.smartcommunitylabdhub.core.components.workflows.factory.Poller;
import it.smartcommunitylabdhub.core.components.workflows.factory.Workflow;

public class PollingService {
    private final Map<String, Poller> pollerMap;

    public PollingService() {
        this.pollerMap = new HashMap<>();
    }

    public void createPoller(String name, List<Workflow> workflowList, long delay, boolean reschedule) {
        Poller poller = new Poller(name, workflowList, delay, reschedule);
        pollerMap.put(name, poller);
    }

    public void startPolling() {
        pollerMap.entrySet().stream().forEach(e -> e.getValue().startPolling());
    }

    public void stopPolling() {
        pollerMap.entrySet().stream().forEach(e -> e.getValue().stopPolling());
    }
}