package it.smartcommunitylabdhub.core.annotations.common;

import it.smartcommunitylabdhub.core.components.infrastructure.factories.specs.SpecEntity;
import org.springframework.stereotype.Component;

import java.lang.annotation.*;

@Retention(RetentionPolicy.RUNTIME)
@Target(ElementType.TYPE)
@Documented
@Component
public @interface SpecType {

    String runtime() default "";

    String kind();

    SpecEntity entity();
}
