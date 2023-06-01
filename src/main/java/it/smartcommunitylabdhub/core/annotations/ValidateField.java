package it.smartcommunitylabdhub.core.annotations;

import java.lang.annotation.*;

import jakarta.validation.Constraint;
import jakarta.validation.Payload;
import it.smartcommunitylabdhub.core.annotations.validators.ValidNameValidator;

@Documented
@Constraint(validatedBy = ValidNameValidator.class)
@Target({ ElementType.PARAMETER, ElementType.FIELD })
@Retention(RetentionPolicy.RUNTIME)
public @interface ValidateField {
    String message() default "Invalid name";

    Class<?>[] groups() default {};

    Class<? extends Payload>[] payload() default {};

    String regex() default "";
}
