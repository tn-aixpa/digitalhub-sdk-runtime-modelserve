package it.smartcommunitylabdhub.core.services.workflows.interfaces;

import java.util.function.Function;

@FunctionalInterface
public interface ConvertFunction<I, O> extends Function<I, O> {
}
