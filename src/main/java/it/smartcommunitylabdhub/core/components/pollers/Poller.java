/**
 * Poller.java
 *
 * This class represents a Poller that facilitates the execution of a list of workflows at specified intervals.
 * It schedules and runs the workflows asynchronously, allowing sequential execution of workflows and optionally
 * rescheduling them after each round of execution.
 */

package it.smartcommunitylabdhub.core.components.pollers;

import java.util.List;
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.CompletionException;
import java.util.concurrent.Executors;
import java.util.concurrent.ScheduledExecutorService;
import java.util.concurrent.TimeUnit;

import it.smartcommunitylabdhub.core.components.workflows.factory.Workflow;
import it.smartcommunitylabdhub.core.exceptions.StopPoller;
import lombok.extern.log4j.Log4j2;

@Log4j2
public class Poller implements Runnable {
    private final List<Workflow> workflowList;
    private ScheduledExecutorService executorService;
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
        log.info("Poller [" + name + "] start: " + Thread.currentThread().getName());
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
                        log.info("POLLER EXCEPTION : " + exception.getMessage());
                        stopPolling();
                    }
                } else {
                    log.info("POLLER EXCEPTION : " + exception.getMessage());
                    stopPolling();
                }
            }

            if (reschedule && active) {
                log.info("Poller [" + name + "] reschedule: " + Thread.currentThread().getName());
                log.info("--------------------------------------------------------------");

                // Delay the rescheduling to ensure all workflows have completed
                getScheduledExecutor().schedule(this::startPolling, delay, TimeUnit.SECONDS);
            }
        });
    }

    private CompletableFuture<Object> executeWorkflowAsync(Workflow workflow) {
        CompletableFuture<Object> workflowExecution = new CompletableFuture<>();

        CompletableFuture.runAsync(() -> {
            try {
                Object result = workflow.execute(null);
                workflowExecution.complete(result);
            } catch (Exception e) {
                workflowExecution.completeExceptionally(e);
            }
        });

        return workflowExecution;
    }

    public void stopPolling() {
        active = false; // Set the flag to false to stop polling
        log.info("Poller [" + name + "] stop: " + Thread.currentThread().getName());
        getScheduledExecutor().shutdown();
        try {
            if (!getScheduledExecutor().awaitTermination(5, TimeUnit.SECONDS)) {
                getScheduledExecutor().shutdownNow();
                if (!getScheduledExecutor().awaitTermination(5, TimeUnit.SECONDS)) {
                    log.error("Unable to shutdown executor service :(");
                }
            }
        } catch (InterruptedException e) {
            getScheduledExecutor().shutdownNow();
            Thread.currentThread().interrupt();
        }
    }
}
