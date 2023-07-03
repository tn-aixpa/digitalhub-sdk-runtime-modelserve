package it.smartcommunitylabdhub.core.config;

import java.util.List;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

import it.smartcommunitylabdhub.core.models.builders.kinds.factory.KindBuilder;
import it.smartcommunitylabdhub.core.models.builders.kinds.factory.KindBuilderFactory;

@Configuration
public class RunBuilderConfig {

    @Bean
    public KindBuilderFactory runBuilderFactory(List<KindBuilder<?, ?>> builders) {
        return new KindBuilderFactory(builders);
    }
}
