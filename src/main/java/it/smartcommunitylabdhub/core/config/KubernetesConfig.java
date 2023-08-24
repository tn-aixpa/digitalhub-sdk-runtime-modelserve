package it.smartcommunitylabdhub.core.config;

import io.fabric8.kubernetes.client.Config;
import io.fabric8.kubernetes.client.ConfigBuilder;
import io.fabric8.kubernetes.client.KubernetesClient;
import io.fabric8.kubernetes.client.KubernetesClientBuilder;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class KubernetesConfig {

    @Value("${kube.config-path}")
    private String configPath;

    @Bean
    KubernetesClient kubernetesClient() {
        try {
            Config config =
                    Config.fromKubeconfig(Files.readString(Path.of(configPath)));
            return new KubernetesClientBuilder().withConfig(config).build();
        } catch (Exception e) {
            return new KubernetesClientBuilder().build();
        }


    }
}
