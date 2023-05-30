package it.smartcommunitylabdhub.core.components.kubernetes.kaniko;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.stream.Collectors;

public class DockerfileGenerator {

    public static String generateDockerfile(DockerBuildConfiguration buildConfig) throws IOException {
        Path templatePath = Path.of(buildConfig.getSourcePath(), "dockerfile-template");
        Path dockerfilePath = Path.of(buildConfig.getTargetPath(), "Dockerfile");

        String templateContent = Files.readString(templatePath);

        String additionalCommands = buildConfig.getAdditionalCommands()
                .stream().map(entry -> entry)
                .collect(Collectors.joining("\n"));

        // Replace placeholders with actual values
        String dockerfileContent = templateContent
                .replace("{{baseImage}}", buildConfig.getBaseImage())
                .replace("{{additionalCommands}}", additionalCommands)
                .replace("{{entrypointCommand}}", buildConfig.getEntrypointCommand());

        // Write the generated Dockerfile
        Files.writeString(dockerfilePath, dockerfileContent);

        return dockerfileContent;
    }
}
