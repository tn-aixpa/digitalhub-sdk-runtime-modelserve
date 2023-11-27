package it.smartcommunitylabdhub.core.models.accessors.utils;

import it.smartcommunitylabdhub.core.models.entities.artifact.ArtifactDTO;

public class ArtifactUtils {

    private ArtifactUtils() {
    }

    public static String getKey(ArtifactDTO artifactDTO) {
        return "store://" + artifactDTO.getProject() + "/artifacts/" + artifactDTO.getKind() + "/"
                + artifactDTO.getName() + ":" + artifactDTO.getId();

    }
}
