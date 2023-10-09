package it.smartcommunitylabdhub.core.repositories;

import java.util.Optional;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Modifying;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import it.smartcommunitylabdhub.core.models.entities.project.Project;

public interface ProjectRepository extends JpaRepository<Project, String> {

    Boolean existsByName(String name);

    @Modifying
    @Query("DELETE FROM Project p WHERE p.name = :name")
    void deleteByName(@Param("name") String name);

    Optional<Project> findByName(String name);

    Page<Project> findAll(Pageable pageable);
}
