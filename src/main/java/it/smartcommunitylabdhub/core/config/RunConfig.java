package it.smartcommunitylabdhub.core.config;

import java.util.List;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

import it.smartcommunitylabdhub.core.components.kinds.factory.builders.KindBuilder;
import it.smartcommunitylabdhub.core.components.kinds.factory.builders.KindBuilderFactory;
import it.smartcommunitylabdhub.core.components.kinds.factory.publishers.KindPublisher;
import it.smartcommunitylabdhub.core.components.kinds.factory.publishers.KindPublisherFactory;
import it.smartcommunitylabdhub.core.components.kinds.factory.workflows.KindWorkflow;
import it.smartcommunitylabdhub.core.components.kinds.factory.workflows.KindWorkflowFactory;

@Configuration
public class RunConfig {

    @Bean
    protected KindBuilderFactory runBuilderFactory(List<KindBuilder<?, ?>> builders) {
        return new KindBuilderFactory(builders);
    }

    @Bean
    protected KindPublisherFactory runPublisherFactory(List<KindPublisher<?, ?>> builders) {
        return new KindPublisherFactory(builders);
    }

    @Bean
    protected KindWorkflowFactory runWorkflowFactory(List<KindWorkflow<?, ?>> builders) {
        return new KindWorkflowFactory(builders);
    }
}
