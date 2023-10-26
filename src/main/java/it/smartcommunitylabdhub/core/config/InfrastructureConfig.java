package it.smartcommunitylabdhub.core.config;

import it.smartcommunitylabdhub.core.components.infrastructure.factories.builders.Builder;
import it.smartcommunitylabdhub.core.components.infrastructure.factories.builders.BuilderFactory;
import it.smartcommunitylabdhub.core.components.infrastructure.factories.frameworks.Framework;
import it.smartcommunitylabdhub.core.components.infrastructure.factories.frameworks.FrameworkFactory;
import it.smartcommunitylabdhub.core.components.infrastructure.factories.runners.Runner;
import it.smartcommunitylabdhub.core.components.infrastructure.factories.runners.RunnerFactory;
import it.smartcommunitylabdhub.core.components.infrastructure.factories.runtimes.Runtime;
import it.smartcommunitylabdhub.core.components.infrastructure.factories.runtimes.RuntimeFactory;
import it.smartcommunitylabdhub.core.components.kinds.factory.builders.KindBuilder;
import it.smartcommunitylabdhub.core.components.kinds.factory.builders.KindBuilderFactory;
import it.smartcommunitylabdhub.core.components.kinds.factory.publishers.KindPublisher;
import it.smartcommunitylabdhub.core.components.kinds.factory.publishers.KindPublisherFactory;
import it.smartcommunitylabdhub.core.components.kinds.factory.workflows.KindWorkflow;
import it.smartcommunitylabdhub.core.components.kinds.factory.workflows.KindWorkflowFactory;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

import java.util.List;

@Configuration
public class InfrastructureConfig {

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

    @Bean
    protected FrameworkFactory frameworkFactory(
            List<Framework<?>> frameworks) {
        return new FrameworkFactory(frameworks);
    }

    @Bean
    protected RuntimeFactory runtimeFactory(
            List<Runtime> runtimes) {
        return new RuntimeFactory(runtimes);
    }

    @Bean
    protected BuilderFactory builderFactory(
            List<Builder> builders) {
        return new BuilderFactory(builders);
    }

    @Bean
    protected RunnerFactory runnerFactory(
            List<Runner> runners) {
        return new RunnerFactory(runners);
    }
}
