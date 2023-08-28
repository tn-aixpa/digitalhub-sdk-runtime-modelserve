package it.smartcommunitylabdhub.core.annotations.validators;

import java.util.UUID;
import it.smartcommunitylabdhub.core.annotations.ValidateField;
import jakarta.validation.ConstraintValidator;
import jakarta.validation.ConstraintValidatorContext;

public class ValidFieldValidator implements ConstraintValidator<ValidateField, String> {

    private String fieldType;
    private String regex;
    private boolean allowNull;

    @Override
    public void initialize(ValidateField constraintAnnotation) {
        regex = constraintAnnotation.regex().isEmpty() ? "^[a-z0-9]([-a-z0-9]*[a-z0-9])?$"
                : constraintAnnotation.regex();

        allowNull = constraintAnnotation.allowNull();
        fieldType = constraintAnnotation.fieldType();
    }

    @Override
    public boolean isValid(String value, ConstraintValidatorContext context) {
        boolean isValid = false;

        if (value == null || value.isEmpty()) {
            return allowNull;
        }

        // Standard string field validation
        if (fieldType.equals("")) {
            isValid = value.matches(regex);
        }

        // Uuid string field
        if (fieldType.equals("uuid")) {
            try {
                UUID uuid = UUID.fromString(value);
                if (uuid.version() == 4) {
                    isValid = true;
                } else {
                    isValid = false;
                }
            } catch (IllegalArgumentException e) {
                isValid = false;
            }
        }

        // if (!isValid) {
        // context.disableDefaultConstraintViolation(); // Disable the default error
        // message
        // context.buildConstraintViolationWithTemplate("Invalid field. It must match
        // the pattern: " + regex)
        // .addConstraintViolation(); // Add a custom error message with the dynamic
        // regex
        // }

        return isValid;
    }
}
