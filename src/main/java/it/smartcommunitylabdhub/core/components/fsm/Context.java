package it.smartcommunitylabdhub.core.components.fsm;

import java.io.Serializable;
import java.util.Optional;

/** Context class */
public class Context<C> implements Cloneable, Serializable {
	Optional<C> value;

	public Context(Optional<C> context) {
		this.value = context;
	}

	public Optional<C> getValue() {
		return value;
	}

	public void setValue(Optional<C> context) {
		this.value = context;
	}

	@Override
	public Object clone() throws CloneNotSupportedException {
		return super.clone();
	}

}
