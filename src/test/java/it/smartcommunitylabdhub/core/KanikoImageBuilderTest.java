package it.smartcommunitylabdhub.core;

import io.fabric8.kubernetes.client.Config;
import io.fabric8.kubernetes.client.ConfigBuilder;
import io.fabric8.kubernetes.client.KubernetesClient;
import io.fabric8.kubernetes.client.KubernetesClientBuilder;
import it.smartcommunitylabdhub.core.components.kubernetes.kaniko.DockerBuildConfiguration;
import it.smartcommunitylabdhub.core.components.kubernetes.kaniko.KanikoImageBuilder;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.test.context.SpringBootTest;

import java.io.IOException;
import java.nio.file.Path;
import java.nio.file.Paths;

import static org.junit.jupiter.api.Assertions.assertEquals;

@SpringBootTest
public class KanikoImageBuilderTest {

    //////////////////////// TO USE THI BUILDER //////////////////////////////
    // HelloWorld.java deve essere messo in /config
    //
    // FROM {{baseImage}}
    //
    // # Add additional instructions here
    // COPY HelloWorld.java /app
    // WORKDIR /app
    // RUN javac HelloWorld.java
    //
    // ENTRYPOINT ["java", "HelloWorld"]
    //
    //////////////////////////////////////

    @Value("${kaniko.source.path}")
    private String kanikoSourcePath;

    @Value("${kaniko.target.path}")
    private String kanikoTargetPath;

    @Test
    void testBuildDockerImage() throws IOException {

        Config config = new ConfigBuilder().withApiVersion("v1").build();
        KubernetesClient client = new KubernetesClientBuilder().withConfig(config).build();

        String basePath = Paths.get(System.getProperty("user.dir")).getParent().toString();

        // Create a sample DockerBuildConfiguration
        DockerBuildConfiguration buildConfig = new DockerBuildConfiguration();
        buildConfig.setDockerTemplatePath(Path.of(basePath, kanikoSourcePath).toString());
        buildConfig.setDockerTargetPath(Path.of(basePath, kanikoTargetPath).toString());
        buildConfig.setBaseImage("openjdk:11");
        buildConfig
                .addCommand("WORKDIR /app")
                .addCommand("COPY . /app")
                .addCommand("RUN javac ./HelloWorld.java");
        buildConfig.setEntrypointCommand("\"java\", \"HelloWorld\"");

        // Invoke the buildDockerImage method
        KanikoImageBuilder.buildDockerImage(client, buildConfig);

        // Assert th`at the Pod and ConfigMap are created
        assertEquals(1, client.pods().inNamespace("default").list().getItems().size());
        assertEquals(1, client.configMaps().inNamespace("default").list().getItems().size());

    }
}
