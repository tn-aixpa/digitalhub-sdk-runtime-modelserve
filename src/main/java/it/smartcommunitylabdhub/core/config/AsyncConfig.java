package it.smartcommunitylabdhub.core.config;

import java.util.concurrent.Executor;
import java.util.concurrent.ThreadPoolExecutor;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.scheduling.annotation.AsyncConfigurer;
import org.springframework.scheduling.annotation.EnableAsync;
import org.springframework.scheduling.concurrent.ThreadPoolTaskExecutor;

import it.smartcommunitylabdhub.core.services.workflows.FunctionWorflowBuilder;
import it.smartcommunitylabdhub.core.services.workflows.PollingService;

@Configuration
@EnableAsync
public class AsyncConfig implements AsyncConfigurer {

    @Bean
    Executor taskExecutor() {
        ThreadPoolTaskExecutor executor = new ThreadPoolTaskExecutor();
        executor.setCorePoolSize(10);
        executor.setMaxPoolSize(20);
        executor.setQueueCapacity(500);
        executor.setThreadNamePrefix("KanikoAsync-");
        executor.setRejectedExecutionHandler(new ThreadPoolExecutor.CallerRunsPolicy());
        executor.initialize();
        return executor;
    }

    @Bean
    PollingService pollingService() {

        // Create new Polling service instance
        PollingService pollingService = new PollingService();

        // Configure Function Workflow
        pollingService.enqueueWorkflow(FunctionWorflowBuilder.buildWorkflow());

        // Configure Artifact Workflow

        // Configure DataItem Workflow

        // Start the polling service
        pollingService.startPolling(5); // Start polling every 5 seconds

        return pollingService;
    }

}
