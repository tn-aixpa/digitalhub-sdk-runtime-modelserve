package it.smartcommunitylabdhub.core.components.infrastructure.factories.runnables;

import java.io.Serializable;

public interface Runnable extends Serializable {
    String framework();

    String getProject();

    String getId();
}
