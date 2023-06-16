package it.smartcommunitylabdhub.core.config;

import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.Executor;
import java.util.concurrent.ThreadPoolExecutor;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.scheduling.annotation.AsyncConfigurer;
import org.springframework.scheduling.annotation.EnableAsync;
import org.springframework.scheduling.concurrent.ThreadPoolTaskExecutor;

import it.smartcommunitylabdhub.core.components.workflows.PollingService;
import it.smartcommunitylabdhub.core.components.workflows.factory.Workflow;
import it.smartcommunitylabdhub.core.components.workflows.functions.FunctionWorkflowBuilder;

@Configuration
@EnableAsync
public class AsyncConfig implements AsyncConfigurer {

    @Bean
    Executor taskExecutor() {
        ThreadPoolTaskExecutor executor = new ThreadPoolTaskExecutor();
        executor.setCorePoolSize(50);
        executor.setMaxPoolSize(100);
        executor.setQueueCapacity(1000);
        executor.setThreadNamePrefix("Async-");
        executor.setRejectedExecutionHandler(new ThreadPoolExecutor.CallerRunsPolicy());
        executor.initialize();
        return executor;
    }

    @Bean
    PollingService pollingService() {

        // Create new Polling service instance
        PollingService pollingService = new PollingService();

        // Create and configure the first poller
        List<Workflow> coreMlrunSyncWorkflow = new ArrayList<>();
        coreMlrunSyncWorkflow.add(FunctionWorkflowBuilder.buildWorkflow());
        // Add workflows to workflowList1

        pollingService.createPoller("DHCore-Mlrun-Sync", coreMlrunSyncWorkflow, 5, true);

        // CREATE OTHER POLLERS
        //
        // List<Workflow> test = new ArrayList<>();
        // Function<Integer, Integer> doubleFunction = num -> {
        // Random randomno = new Random();
        // long randomDelay = (long) (randomno.nextDouble() * 7 + 3); // Random delay
        // between 3 and 10
        // // seconds
        // System.out.println("RANDOM DELAY TEST WORKFLOW " + randomDelay);
        // try {
        // Thread.sleep(randomDelay * 1000);
        // } catch (InterruptedException e) {
        // // Handle interrupted exception if necessary
        // }

        // return 9;
        // };
        // test.add(WorkflowFactory
        // .builder().step(doubleFunction, 5).build());
        // pollingService.createPoller("TEST-POLLER", test, 3, true);

        // Start polling
        pollingService.startPolling();

        return pollingService;
    }

}
