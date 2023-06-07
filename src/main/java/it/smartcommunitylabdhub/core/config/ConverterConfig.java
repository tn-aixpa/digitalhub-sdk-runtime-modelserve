package it.smartcommunitylabdhub.core.config;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

import it.smartcommunitylabdhub.core.models.converters.CommandFactory;
import it.smartcommunitylabdhub.core.models.converters.ConverterFactoryImpl;
import it.smartcommunitylabdhub.core.models.converters.interfaces.ConverterFactory;
import it.smartcommunitylabdhub.core.models.converters.types.ArtifactConverter;
import it.smartcommunitylabdhub.core.models.converters.types.CBORConverter;
import it.smartcommunitylabdhub.core.models.converters.types.DataItemConverter;
import it.smartcommunitylabdhub.core.models.converters.types.DateTimeConverter;
import it.smartcommunitylabdhub.core.models.converters.types.FunctionConverter;
import it.smartcommunitylabdhub.core.models.converters.types.IntegerConverter;
import it.smartcommunitylabdhub.core.models.converters.types.LogConverter;
import it.smartcommunitylabdhub.core.models.converters.types.ProjectConverter;
import it.smartcommunitylabdhub.core.models.converters.types.RunConverter;
import it.smartcommunitylabdhub.core.models.converters.types.WorkflowConverter;

@Configuration
public class ConverterConfig {

    @Bean
    ConverterFactory converterFactory() {
        ConverterFactoryImpl factory = new ConverterFactoryImpl();

        // Register converter
        factory.registerConverter("function", FunctionConverter::new);
        factory.registerConverter("artifact", ArtifactConverter::new);
        factory.registerConverter("dataitem", DataItemConverter::new);
        factory.registerConverter("workflow", WorkflowConverter::new);
        factory.registerConverter("project", ProjectConverter::new);
        factory.registerConverter("cbor", CBORConverter::new);
        factory.registerConverter("integer", IntegerConverter::new);
        factory.registerConverter("datetime", DateTimeConverter::new);
        factory.registerConverter("run", RunConverter::new);
        factory.registerConverter("log", LogConverter::new);

        return factory;
    }

    @Bean
    CommandFactory commandFactory(ConverterFactory converterFactory) {
        return new CommandFactory(converterFactory);
    }

}
