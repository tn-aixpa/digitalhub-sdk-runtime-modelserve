/**
 * KindInfrastructure.java
 *
 */

package it.smartcommunitylabdhub.core.components.infrastructure.factories.frameworks;

public interface Framework<R extends Runnable> {

	void execute(Runnable runnable);
}
