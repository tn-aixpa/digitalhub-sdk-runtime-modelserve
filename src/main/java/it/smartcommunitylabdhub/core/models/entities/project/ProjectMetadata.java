package it.smartcommunitylabdhub.core.models.entities.project;

import io.micrometer.common.lang.NonNull;
import it.smartcommunitylabdhub.core.models.base.Metadata;
import jakarta.validation.constraints.NotNull;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;


@AllArgsConstructor
@NoArgsConstructor
@Getter
@Setter
public class ProjectMetadata extends Metadata {
	@NonNull
	String name;
	@NotNull
	String description;

}
