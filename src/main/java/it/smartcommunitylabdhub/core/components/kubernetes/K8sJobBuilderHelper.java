package it.smartcommunitylabdhub.core.components.kubernetes;

import io.kubernetes.client.openapi.models.V1EnvVar;
import org.springframework.stereotype.Component;

import java.util.ArrayList;
import java.util.List;

/**
 * Helper class for building Kubernetes job environment variables.
 * This class provides methods to retrieve environment variables with fallback values
 * and constructs a list of V1EnvVar objects for use in Kubernetes job specifications.
 */
@Component
public class K8sJobBuilderHelper {

    /**
     * A helper method to get an environment variable with a default value if not present.
     *
     * @param variableName The name of the environment variable.
     * @param defaultValue The default value to use if the environment variable is not present.
     * @return The value of the environment variable if present, otherwise the defaultValue.
     */
    private String getEnvVariable(String variableName, String defaultValue) {
        // Access the environment variable using System.getenv()
        String value = System.getenv(variableName);
        // Use the value from the system environment if available, otherwise use the defaultValue
        return (value != null && !value.isEmpty()) ? value : defaultValue;
    }

    /**
     * Method to retrieve a list of V1EnvVar containing environment variables for a Kubernetes job.
     *
     * @return A list of V1EnvVar objects representing environment variables for a Kubernetes job.
     */
    public List<V1EnvVar> getEnvV1() {
        // Create a list to hold V1EnvVar objects
        return new ArrayList<>(List.of(
                // Add environment variables with their names and values
                new V1EnvVar().name("DHUB_CORE_ENDPOINT").value(getEnvVariable("DHUB_CORE_ENDPOINT", "http://192.168.49.1:8080")),
                new V1EnvVar().name("AWS_ACCESS_KEY_ID").value(getEnvVariable("AWS_ACCESS_KEY_ID", "minio")),
                new V1EnvVar().name("AWS_SECRET_ACCESS_KEY").value(getEnvVariable("AWS_SECRET_ACCESS_KEY", "minio123")),
                new V1EnvVar().name("S3_ENDPOINT_URL").value(getEnvVariable("S3_ENDPOINT_URL", "http://192.168.49.2:30080")),
                new V1EnvVar().name("S3_ACCESS_KEY_ID").value(getEnvVariable("S3_ACCESS_KEY_ID", "minio")),
                new V1EnvVar().name("S3_SECRET_ACCESS_KEY").value(getEnvVariable("S3_SECRET_ACCESS_KEY", "minio123")),
                new V1EnvVar().name("S3_BUCKET_NAME").value(getEnvVariable("S3_BUCKET_NAME", "mlrun")),
                new V1EnvVar().name("POSTGRES_HOST").value(getEnvVariable("POSTGRES_HOST", "192.168.49.1")),
                new V1EnvVar().name("POSTGRES_PORT").value(getEnvVariable("POSTGRES_PORT", "5433")),
                new V1EnvVar().name("POSTGRES_DATABASE").value(getEnvVariable("POSTGRES_DATABASE", "dbt")),
                new V1EnvVar().name("POSTGRES_USER").value(getEnvVariable("POSTGRES_USER", "testuser")),
                new V1EnvVar().name("POSTGRES_PASSWORD").value(getEnvVariable("POSTGRES_PASSWORD", "testpassword")),
                new V1EnvVar().name("POSTGRES_SCHEMA").value(getEnvVariable("POSTGRES_SCHEMA", "public"))
        ));
    }
}
