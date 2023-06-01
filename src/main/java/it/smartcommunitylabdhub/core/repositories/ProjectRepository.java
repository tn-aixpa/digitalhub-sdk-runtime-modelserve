package it.smartcommunitylabdhub.core.repositories;

import java.util.Optional;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;

import it.smartcommunitylabdhub.core.models.entities.Project;

public interface ProjectRepository extends JpaRepository<Project, String> {

    Boolean existsByName(String name);

    void deleteByName(String name);

    Optional<Project> findByName(String name);

    Page<Project> findAll(Pageable pageable);
}
