package it.smartcommunitylabdhub.core.components.kubernetes.kaniko;

import java.io.FileReader;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.Map;
import java.util.stream.Collectors;
import java.util.stream.Stream;

public class DockerfileGenerator {
    public static String generateDockerfile(DockerBuildConfiguration buildConfig) throws IOException {
        Path templatePath = Path.of("src/main/resources/config/dockerfile-template");
        Path dockerfilePath = Path.of("src/main/resources/config/Dockerfile");

        Stream<String> lines = Files.lines(templatePath, StandardCharsets.UTF_8);
        // Read the Dockerfile template
        String templateContent = Files.readString(templatePath);

        String additionalCommands = buildConfig.getAdditionalProperties()
                .entrySet()
                .stream().map(entry -> entry.getKey() + " " + entry.getValue().toString())
                .collect(Collectors.joining("\n"));

        // Replace placeholders with actual values
        String dockerfileContent = templateContent
                .replace("{{baseImage}}", buildConfig.getBaseImage())
                .replace("{{additionalCommand}}", additionalCommands)
                .replace("{{entrypointCommand}}", buildConfig.getEntrypointCommand());

        // Add extra commands
        for (Map.Entry<String, Object> entry : buildConfig.getAdditionalProperties().entrySet()) {
            String command = entry.getKey();
            dockerfileContent += "\n" + command;
        }

        // Write the generated Dockerfile
        Files.writeString(dockerfilePath, dockerfileContent);

        return dockerfileContent;
    }
}
