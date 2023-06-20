package it.smartcommunitylabdhub.core.config;

import java.util.List;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

import it.smartcommunitylabdhub.core.models.builders.runs.RunBuilder;
import it.smartcommunitylabdhub.core.models.builders.runs.RunBuilderFactory;

@Configuration
public class RunBuilderConfig {

    @Bean
    public RunBuilderFactory runBuilderFactory(List<RunBuilder> builders) {
        return new RunBuilderFactory(builders);
    }
}