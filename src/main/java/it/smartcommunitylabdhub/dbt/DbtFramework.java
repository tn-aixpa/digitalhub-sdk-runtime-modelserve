package it.smartcommunitylabdhub.dbt;

import it.smartcommunitylabdhub.core.annotations.FrameworkComponent;
import it.smartcommunitylabdhub.core.components.infrastructure.factories.frameworks.Framework;

@FrameworkComponent(runtime = "dbt", task = "job")
public class DbtFramework<R extends Runnable> implements Framework<R> {

	@Override
	public void execute(Runnable runnable) {
		// TODO Auto-generated method stub
		throw new UnsupportedOperationException("Unimplemented method 'execute'");
	}


}
