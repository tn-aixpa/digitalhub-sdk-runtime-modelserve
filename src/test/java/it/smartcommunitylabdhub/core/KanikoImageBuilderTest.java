package it.smartcommunitylabdhub.core;

import io.fabric8.kubernetes.client.DefaultKubernetesClient;
import io.fabric8.kubernetes.client.KubernetesClient;
import io.fabric8.kubernetes.client.server.mock.KubernetesServer;
import it.smartcommunitylabdhub.core.components.kubernetes.kaniko.DockerBuildConfiguration;
import it.smartcommunitylabdhub.core.components.kubernetes.kaniko.KanikoImageBuilder;

import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import java.io.IOException;

import static org.junit.jupiter.api.Assertions.assertEquals;

public class KanikoImageBuilderTest {
    KubernetesClient client = new DefaultKubernetesClient();

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

    @Test
    void testBuildDockerImage() throws IOException {
        // Create a sample DockerBuildConfiguration
        DockerBuildConfiguration buildConfig = new DockerBuildConfiguration();
        buildConfig.setBaseImage("openjdk:11");
        buildConfig.setAdditionalProperty("COPY", "HelloWorld.java /app");
        buildConfig.setAdditionalProperty("WORKDIR", "/app");
        buildConfig.setAdditionalProperty("RUN", "javac HelloWorld.java");
        buildConfig.setEntrypointCommand("java HelloWorld");

        // Invoke the buildDockerImage method
        KanikoImageBuilder.buildDockerImage(client, buildConfig);

        // Assert that the Pod and ConfigMap are created
        assertEquals(1, client.pods().inNamespace("default").list().getItems().size());
        assertEquals(1, client.configMaps().inNamespace("default").list().getItems().size());

    }
}
