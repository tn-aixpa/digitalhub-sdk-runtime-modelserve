package it.smartcommunitylabdhub.core.models.base;

import java.io.Serializable;
import java.util.Date;
import org.hibernate.annotations.CreationTimestamp;
import org.hibernate.annotations.UpdateTimestamp;
import it.smartcommunitylabdhub.core.annotations.validators.ValidateField;
import jakarta.persistence.Column;
import jakarta.validation.constraints.NotEmpty;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

@AllArgsConstructor
@NoArgsConstructor
@Getter
@Setter
public class Metadata implements Serializable {

	@NotEmpty
	@ValidateField
	String project;

	@CreationTimestamp
	@Column(updatable = false)
	private Date created;

	@UpdateTimestamp
	private Date updated;

}
