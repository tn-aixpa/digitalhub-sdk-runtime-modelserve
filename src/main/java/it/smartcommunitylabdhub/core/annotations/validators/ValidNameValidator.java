package it.smartcommunitylabdhub.core.annotations.validators;

import java.util.regex.Pattern;

import it.smartcommunitylabdhub.core.annotations.ValidName;
import jakarta.validation.ConstraintValidator;
import jakarta.validation.ConstraintValidatorContext;

public class ValidNameValidator implements ConstraintValidator<ValidName, String> {

    private static final Pattern NAME_PATTERN = Pattern.compile("^[a-z0-9]([-a-z0-9]*[a-z0-9])?$");

    @Override
    public boolean isValid(String value, ConstraintValidatorContext context) {
        return value == null || NAME_PATTERN.matcher(value).matches();
    }
}