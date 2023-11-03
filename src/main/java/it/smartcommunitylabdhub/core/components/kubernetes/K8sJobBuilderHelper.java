package it.smartcommunitylabdhub.core.components.kubernetes;

import io.fabric8.kubernetes.api.model.EnvVar;
import io.kubernetes.client.openapi.models.V1EnvVar;
import org.springframework.stereotype.Component;

import java.util.ArrayList;
import java.util.List;

@Component
public class K8sJobBuilderHelper {

    // @Autowired
    // Environment environment;

    public List<EnvVar> getEnv() {
        return new ArrayList<>(List.of(
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
    }

    public List<V1EnvVar> getEnvV1() {
        return new ArrayList<>(List.of(
                new V1EnvVar().name("DHUB_CORE_ENDPOINT").value("http://192.168.49.1:8080"),
                new V1EnvVar().name("AWS_ACCESS_KEY_ID").value("minio"),
                new V1EnvVar().name("AWS_SECRET_ACCESS_KEY").value("minio123"),
                new V1EnvVar().name("S3_ENDPOINT_URL").value("http://192.168.49.2:30080"),
                new V1EnvVar().name("S3_ACCESS_KEY_ID").value("minio"),
                new V1EnvVar().name("S3_SECRET_ACCESS_KEY").value("minio123"),
                new V1EnvVar().name("S3_BUCKET_NAME").value("mlrun"),
                new V1EnvVar().name("POSTGRES_HOST").value("192.168.49.1"),
                new V1EnvVar().name("POSTGRES_PORT").value("5433"),
                new V1EnvVar().name("POSTGRES_DATABASE").value("dbt"),
                new V1EnvVar().name("POSTGRES_USER").value("testuser"),
                new V1EnvVar().name("POSTGRES_PASSWORD").value("testpassword"),
                new V1EnvVar().name("POSTGRES_SCHEMA").value("public")));
    }

}
