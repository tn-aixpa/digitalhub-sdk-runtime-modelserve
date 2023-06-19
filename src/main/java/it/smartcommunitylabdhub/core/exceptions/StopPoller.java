package it.smartcommunitylabdhub.core.exceptions;

public class StopPoller extends RuntimeException {

    public StopPoller(String message) {
        super(message);
    }
}
