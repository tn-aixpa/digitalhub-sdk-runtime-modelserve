package it.smartcommunitylabdhub.core.annotations;

import java.lang.annotation.*;

import jakarta.validation.Constraint;
import jakarta.validation.Payload;
import it.smartcommunitylabdhub.core.annotations.validators.ValidFieldValidator;

@Documented
@Constraint(validatedBy = ValidFieldValidator.class)
@Target({ ElementType.PARAMETER, ElementType.FIELD })
@Retention(RetentionPolicy.RUNTIME)
public @interface ValidateField {
    String message() default "";

    Class<?>[] groups() default {};

    Class<? extends Payload>[] payload() default {};

    String regex() default "";
}
