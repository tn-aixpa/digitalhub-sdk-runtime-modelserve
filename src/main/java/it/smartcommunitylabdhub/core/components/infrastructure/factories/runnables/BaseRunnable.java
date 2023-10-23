package it.smartcommunitylabdhub.core.components.infrastructure.factories.runnables;

import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
public abstract class BaseRunnable implements Runnable {
	String project;
	String id;
}
