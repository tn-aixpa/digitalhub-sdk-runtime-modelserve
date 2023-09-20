package it.smartcommunitylabdhub.core.components.kubernetes;

import java.util.ArrayList;
import java.util.List;
// import org.springframework.beans.factory.annotation.Autowired;
// import org.springframework.core.env.Environment;
import org.springframework.stereotype.Component;
import io.fabric8.kubernetes.api.model.EnvVar;

@Component
public class K8sJobBuilderHelper {

	// @Autowired
	// Environment environment;

	public List<EnvVar> getEnv() {
		List<EnvVar> envVars = new ArrayList<>();
		envVars.addAll(
				List.of(
						new EnvVar("DHUB_CORE_ENDPOINT", "http://192.168.49.1:8080", null),
						new EnvVar("AWS_ACCESS_KEY_ID", "minio", null),
						new EnvVar("AWS_SECRET_ACCESS_KEY", "minio123", null),
						new EnvVar("S3_ENDPOINT_URL", "http://192.168.49.2:30080", null),
						new EnvVar("S3_ACCESS_KEY_ID", "minio", null),
						new EnvVar("S3_SECRET_ACCESS_KEY", "minio123", null),
						new EnvVar("S3_BUCKET_NAME", "mlrun", null),
						new EnvVar("POSTGRES_HOST", "192.168.49.1", null),
						new EnvVar("POSTGRES_PORT", "5433", null),
						new EnvVar("POSTGRES_DATABASE", "dbt", null),
						new EnvVar("POSTGRES_USER", "testuser", null),
						new EnvVar("POSTGRES_PASSWORD", "testpassword", null),
						new EnvVar("POSTGRES_SCHEMA", "public", null)));
		return envVars;
	}

}
