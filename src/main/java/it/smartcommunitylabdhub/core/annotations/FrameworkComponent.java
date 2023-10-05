package it.smartcommunitylabdhub.core.annotations;

import java.lang.annotation.Documented;
import java.lang.annotation.ElementType;
import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;
import java.lang.annotation.Target;

import org.springframework.stereotype.Component;

@Retention(RetentionPolicy.RUNTIME)
@Target(ElementType.TYPE)
@Documented
@Component
public @interface FrameworkComponent {
    String runtime(); // runtime can be dbt, nefertem, dss, kfp...

    String task(); // define the task type that have to be executed by the framework for
                   // a specific runtime

    String name() default ""; // framework take care to create the component for the context
    // execution local, serve, deploy

}
