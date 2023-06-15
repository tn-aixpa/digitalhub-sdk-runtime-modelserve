package it.smartcommunitylabdhub.core.repositories;

import java.util.List;
import java.util.Optional;

import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Modifying;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

import it.smartcommunitylabdhub.core.models.entities.Artifact;

public interface ArtifactRepository extends JpaRepository<Artifact, String> {
        List<Artifact> findByProject(String project);

        Page<Artifact> findAll(Pageable pageable);

        ////////////////////////////
        // CONTEXT SPECIFIC QUERY //
        ////////////////////////////

        Page<Artifact> findAllByProjectAndNameOrderByCreatedDesc(String project, String name, Pageable pageable);

        @Query("SELECT a FROM Artifact a WHERE a.project = :project AND (a.name, a.project, a.created) IN " +
                        "(SELECT a2.name, a2.project, MAX(a2.created) FROM Artifact a2 WHERE a2.project = :project GROUP BY a2.name, a2.project) "
                        +
                        "ORDER BY a.created DESC")
        Page<Artifact> findAllLatestArtifactsByProject(@Param("project") String project, Pageable pageable);

        Optional<Artifact> findByProjectAndNameAndId(@Param("project") String project, @Param("name") String name,
                        @Param("id") String id);

        @Query("SELECT a FROM Artifact a WHERE a.project = :project AND a.name = :name " +
                        "AND a.created = (SELECT MAX(a2.created) FROM Artifact a2 WHERE a2.project = :project AND a2.name = :name)")
        Optional<Artifact> findLatestArtifactByProjectAndName(@Param("project") String project,
                        @Param("name") String name);

        boolean existsByProjectAndNameAndId(String project, String name, String id);

        @Modifying
        @Query("DELETE FROM Artifact a WHERE a.project = :project AND a.name = :name AND a.id = :id")
        void deleteByProjectAndNameAndId(@Param("project") String project, @Param("name") String name,
                        @Param("id") String id);

        boolean existsByProjectAndName(String project, String name);

        @Modifying
        @Query("DELETE FROM Artifact a WHERE a.project = :project AND a.name = :name ")
        void deleteByProjectAndName(@Param("project") String project, @Param("name") String name);

        @Modifying
        @Query("DELETE FROM Artifact a WHERE a.project = :project ")
        void deleteByProjectName(@Param("project") String project);

}
