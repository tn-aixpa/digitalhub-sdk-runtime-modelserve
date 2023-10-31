package it.smartcommunitylabdhub.core.annotations.common;

import it.smartcommunitylabdhub.core.components.infrastructure.factories.specs.SpecEntity;
import org.springframework.stereotype.Indexed;

import java.lang.annotation.ElementType;
import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;
import java.lang.annotation.Target;

@Retention(RetentionPolicy.RUNTIME)
@Target(ElementType.TYPE)
@Indexed
public @interface SpecType {
    String kind();

    SpecEntity entity();
}
