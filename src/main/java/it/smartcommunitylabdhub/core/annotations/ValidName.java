package it.smartcommunitylabdhub.core.annotations;

import java.lang.annotation.*;

import jakarta.validation.Constraint;
import jakarta.validation.Payload;
import it.smartcommunitylabdhub.core.annotations.validators.ValidNameValidator;

@Constraint(validatedBy = ValidNameValidator.class)
@Retention(RetentionPolicy.RUNTIME)
@Target(ElementType.PARAMETER)
public @interface ValidName {

    String message() default "Invalid name format";

    Class<?>[] groups() default {};

    Class<? extends Payload>[] payload() default {};
}
