package it.smartcommunitylabdhub.core;

import static org.junit.Assert.assertNotNull;
import static org.junit.Assert.assertTrue;

import org.junit.Test;

import io.fabric8.kubernetes.api.model.batch.v1.Job;
import io.fabric8.kubernetes.api.model.batch.v1.JobBuilder;
import io.fabric8.kubernetes.client.DefaultKubernetesClient;
import io.fabric8.kubernetes.client.KubernetesClient;
import io.fabric8.kubernetes.client.server.mock.EnableKubernetesMockClient;

@EnableKubernetesMockClient
public class KubernetesTests {
    KubernetesClient kubernetesClient = new DefaultKubernetesClient();

    @Test
    public void helloWorldJob() {
        Job job = new JobBuilder()
                .withNewMetadata()
                .withName("hello-job")
                .endMetadata()
                .withNewSpec()
                .withNewTemplate()
                .withNewSpec()
                .addNewContainer()
                .withName("hello-container")
                .withImage("busybox")
                .withCommand("echo", "Hello, World!")
                .endContainer()
                .withRestartPolicy("Never")
                .endSpec()
                .endTemplate()
                .endSpec()
                .build();

        kubernetesClient.resource(job).inNamespace("default").create();

        Job createdJob = kubernetesClient.batch().v1().jobs().inNamespace("default").withName("hello-job").get();
        assertNotNull(createdJob);

        Job jobStatus = kubernetesClient.batch().v1().jobs().inNamespace("default").withName("hello-job").get();
        assertNotNull(jobStatus.getStatus());

        String jobLogs = kubernetesClient.batch().v1().jobs().inNamespace("default").withName("hello-job").getLog();
        assertNotNull(jobLogs);
        assertTrue(jobLogs.contains("Hello, World!"));

    }
}
