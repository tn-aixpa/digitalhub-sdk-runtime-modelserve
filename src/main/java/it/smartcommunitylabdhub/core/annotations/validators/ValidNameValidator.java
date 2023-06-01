package it.smartcommunitylabdhub.core.annotations.validators;

import java.util.regex.Pattern;

import it.smartcommunitylabdhub.core.annotations.ValidateField;
import jakarta.validation.ConstraintValidator;
import jakarta.validation.ConstraintValidatorContext;

public class ValidNameValidator implements ConstraintValidator<ValidateField, String> {

    private String regex;

    @Override
    public void initialize(ValidateField constraintAnnotation) {
        regex = constraintAnnotation.regex().isEmpty() ? "^[a-z0-9]([-a-z0-9]*[a-z0-9])?$"
                : constraintAnnotation.regex();
    }

    @Override
    public boolean isValid(String value, ConstraintValidatorContext context) {
        if (value == null) {
            return false;
        }

        boolean isValid = value.matches(regex);

        if (!isValid) {
            context.disableDefaultConstraintViolation(); // Disable the default error message
            context.buildConstraintViolationWithTemplate("Invalid field. It must match the pattern: " + regex)
                    .addConstraintViolation(); // Add a custom error message with the dynamic regex

        }
        return isValid;

    }
}
