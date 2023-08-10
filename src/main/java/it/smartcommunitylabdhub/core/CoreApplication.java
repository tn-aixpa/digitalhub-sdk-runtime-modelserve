package it.smartcommunitylabdhub.core;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.ComponentScan;

@SpringBootApplication
@ComponentScan({ "it.smartcommunitylabdhub.core", "it.smartcommunitylabdhub.mlrun", "it.smartcommunitylabdhub.dbt" })
public class CoreApplication {

	public static void main(String[] args) {
		SpringApplication.run(CoreApplication.class, args);
	}

}
