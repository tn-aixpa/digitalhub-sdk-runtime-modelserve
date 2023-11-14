package it.smartcommunitylabdhub.core.components.kubernetes;

import io.kubernetes.client.openapi.models.V1EnvVar;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;

/**
 * Helper class for building Kubernetes job environment variables.
 * This class provides methods to retrieve environment variables with fallback values
 * and constructs a list of V1EnvVar objects for use in Kubernetes job specifications.
 */
@Component
public class K8sJobBuilderHelper {

    @Value("${application.endpoint}")
    private String DH_ENDPOINT;

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

        System.getenv();
        // Use the value from the system environment if available, otherwise use the defaultValue
        return (value != null && !value.isEmpty()) ? value : defaultValue;
    }

    /**
     * Method to retrieve a list of V1EnvVar containing environment variables for a Kubernetes job.
     *
     * @return A list of V1EnvVar objects representing environment variables for a Kubernetes job.
     */

    public List<V1EnvVar> getEnvV1() {

        List<V1EnvVar> envVarList = new ArrayList<>();

        // Iterate over all environment variables
        for (Map.Entry<String, String> entry : System.getenv().entrySet()) {
            String variableName = entry.getKey();
            String variableValue = entry.getValue();

            // Check if the variable has the "DH_" prefix
            if (variableName.startsWith("DH_")) {

                // Remove the "DH_" prefix and add to the list
                String strippedName = variableName.substring("DH_".length());
                envVarList.add(new V1EnvVar().name(strippedName).value(variableValue));
            }
        }

        // Add extra envs
        envVarList.add(new V1EnvVar().name("DHUB_CORE_ENDPOINT")
                .value(DH_ENDPOINT));

        return envVarList;


//                DHCORE_AWS_ACCESS_KEY_ID"="minio"
//                DHCORE_AWS_SECRET_ACCESS_KEY="minio123"
//                DHCORE_S3_ENDPOINT_URL="http://192.168.49.2:30080"
//                DHCORE_S3_ACCESS_KEY_ID="minio"
//                DHCORE_S3_SECRET_ACCESS_KEY="minio123"
//                DHCORE_S3_BUCKET_NAME="mlrun"
//                DHCORE_POSTGRES_HOST="192.168.49.1"
//                DHCORE_POSTGRES_PORT="5433"
//                DHCORE_POSTGRES_DATABASE="dbt"
//                DHCORE_POSTGRES_USER="testuser"
//                DHCORE_POSTGRES_PASSWORD="testpassword"
//                DHCORE_POSTGRES_SCHEMA="public"

    }
}