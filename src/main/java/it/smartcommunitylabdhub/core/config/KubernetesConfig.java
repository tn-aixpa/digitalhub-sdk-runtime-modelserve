package it.smartcommunitylabdhub.core.config;

import io.fabric8.kubernetes.client.Config;
import io.fabric8.kubernetes.client.ConfigBuilder;
import io.fabric8.kubernetes.client.KubernetesClient;
import io.fabric8.kubernetes.client.KubernetesClientBuilder;
import io.kubernetes.client.openapi.ApiClient;
import io.kubernetes.client.util.ClientBuilder;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class KubernetesConfig {

    @Value("${fabric8.kube.master-url}")
    private String masterUrl;

    @Value("${fabric8.kube.ca-cert-file}")
    private String caCertFile;

    @Value("${fabric8.kube.client-cert-file}")
    private String clientCertFile;

    @Value("${fabric8.kube.client-key-file}")
    private String clientKeyFile;


    @Bean
    KubernetesClient kubernetesClient() {
        try {
            Config config = new ConfigBuilder()
                    .withMasterUrl(masterUrl) // Add your MasterUrl (ex: minikube ip)
                    .withCaCertFile(caCertFile) // Replace with your ca.crt path
                    .withClientCertFile(clientCertFile) // Replace with your client.crt path
                    .withClientKeyFile(clientKeyFile) // Replace with your client.key path
                    .build();

            return new KubernetesClientBuilder()
                    .withConfig(config).build();
        } catch (Exception e) {
            return new KubernetesClientBuilder().build();
        }
    }

    // @Bean
    // ApiClient kubeApiClient() throws Exception {

    // try {
    // // ClientBuilder.fromCertificateSigningRequest()
    // // KubeConfig
    // // ApiClient client = io.kubernetes.client.util.Config.fromConfig(null);


    // throw new Exception();

    // } catch (Exception e) {

    // return ClientBuilder.standard().build();

    // }
    // }
}
