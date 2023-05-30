package it.smartcommunitylabdhub.core.repositories;

import java.util.List;

import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;

import it.smartcommunitylabdhub.core.models.entities.Artifact;

public interface ArtifactRepository extends JpaRepository<Artifact, String> {
    List<Artifact> findByProject(String project);

    Page<Artifact> findAll(Pageable pageable);

    Page<Artifact> findAllByProjectAndName(String project, String name, Pageable pageable);
}
