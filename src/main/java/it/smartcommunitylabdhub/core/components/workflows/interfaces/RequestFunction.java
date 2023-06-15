package it.smartcommunitylabdhub.core.components.workflows.interfaces;

import java.util.function.Function;

@FunctionalInterface
public interface RequestFunction<I, O> extends Function<I, O> {
}
