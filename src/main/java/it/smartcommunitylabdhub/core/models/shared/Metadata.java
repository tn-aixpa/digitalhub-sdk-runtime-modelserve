package it.smartcommunitylabdhub.core.models.shared;

import java.util.Date;
import org.hibernate.annotations.CreationTimestamp;
import org.hibernate.annotations.UpdateTimestamp;
import it.smartcommunitylabdhub.core.annotations.ValidateField;
import jakarta.persistence.Column;
import jakarta.validation.constraints.NotNull;

public class Metadata {

	@NotNull
	@ValidateField
	String project;

	@CreationTimestamp
	@Column(updatable = false)
	private Date created;

	@UpdateTimestamp
	private Date updated;

}
