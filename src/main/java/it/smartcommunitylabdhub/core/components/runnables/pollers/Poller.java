package it.smartcommunitylabdhub.core.components.runnables.pollers;

import java.util.List;
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.CompletionException;
import java.util.concurrent.Executors;
import java.util.concurrent.ScheduledExecutorService;
import java.util.concurrent.TimeUnit;

import it.smartcommunitylabdhub.core.components.runnables.pollers.workflows.factory.Workflow;
import it.smartcommunitylabdhub.core.exceptions.StopPoller;

public class Poller implements Runnable {
    private final List<Workflow> workflowList;
    private transient ScheduledExecutorService executorService;
    private final long delay;
    private final boolean reschedule;
    private final String name;
    private boolean active;

    public Poller(String name, List<Workflow> workflowList, long delay, boolean reschedule) {
        this.name = name;
        this.workflowList = workflowList;
        this.delay = delay;
        this.reschedule = reschedule;
        this.active = true;
    }

    ScheduledExecutorService getScheduledExecutor() {
        if (this.executorService == null) {
            this.executorService = Executors.newSingleThreadScheduledExecutor();
        }
        return this.executorService;
    }

    public void startPolling() {
        System.out.println("Poller [" + name + "] start: " + Thread.currentThread().getName());
        getScheduledExecutor().schedule(this, delay, TimeUnit.SECONDS);
    }

    @Override
    public void run() {
        CompletableFuture<Object> allWorkflowsFuture = CompletableFuture.completedFuture(null);

        // Execute the workflows sequentially
        for (Workflow workflow : workflowList) {
            if (active) {
                allWorkflowsFuture = allWorkflowsFuture.thenComposeAsync(result -> executeWorkflowAsync(workflow));
            } else {
                break;
            }
        }

        allWorkflowsFuture.whenComplete((result, exception) -> {
            if (exception != null) {
                if (exception instanceof CompletionException) {
                    Throwable cause = exception.getCause();
                    if (cause instanceof StopPoller) {
                        stopPolling(); // Stop this Poller thread.
                    } else {
                        System.out.println("POLLER EXCEPTION : " + exception.getMessage());
                        stopPolling();
                    }
                } else {
                    System.out.println("POLLER EXCEPTION : " + exception.getMessage());
                    stopPolling();
                }
            }

            if (reschedule && active) {
                System.out.println("Poller [" + name + "] reschedule: " + Thread.currentThread().getName());
                System.out.println("-------------------------------------------------------------------");

                // Delay the rescheduling to ensure all workflows have completed
                getScheduledExecutor().schedule(() -> startPolling(), delay, TimeUnit.SECONDS);
            }
        });
    }

    private CompletableFuture<Object> executeWorkflowAsync(Workflow workflow) {
        CompletableFuture<Object> workflowExecution = new CompletableFuture<>();

        CompletableFuture.runAsync(() -> {
            try {
                Object result = workflow.execute(null);
                // System.out.println(result.toString());
                workflowExecution.complete(result);
            } catch (Exception e) {
                workflowExecution.completeExceptionally(e);
            }
        });

        return workflowExecution;
    }

    public void stopPolling() {
        active = false; // Set the flag to false to stop polling
        System.out.println("Poller [" + name + "] stop: " + Thread.currentThread().getName());
        getScheduledExecutor().shutdown();
        try {
            if (!getScheduledExecutor().awaitTermination(5, TimeUnit.SECONDS)) {
                getScheduledExecutor().shutdownNow();
                if (!getScheduledExecutor().awaitTermination(5, TimeUnit.SECONDS)) {
                    System.err.println("Unable to shutdown executor service :(");
                }
            }
        } catch (InterruptedException e) {
            getScheduledExecutor().shutdownNow();
            Thread.currentThread().interrupt();
        }
    }
}
