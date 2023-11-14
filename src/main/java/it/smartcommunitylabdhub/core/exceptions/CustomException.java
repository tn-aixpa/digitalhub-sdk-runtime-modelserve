package it.smartcommunitylabdhub.core.exceptions;

import lombok.Getter;

@Getter
public class CustomException extends RuntimeException {
    private final Exception innerException;

    public CustomException(String message, Exception innerException) {
        super(message);
        this.innerException = innerException;
    }

}
