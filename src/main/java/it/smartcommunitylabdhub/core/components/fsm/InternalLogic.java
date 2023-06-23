package it.smartcommunitylabdhub.core.components.fsm;

import java.io.Serializable;
import java.util.Optional;

@FunctionalInterface
public interface InternalLogic<I, C> extends Serializable {
    Optional<?> apply(I input, C context);
}
