package it.smartcommunitylabdhub.core.repositories;

import java.util.List;
import java.util.Optional;

import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Modifying;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

import it.smartcommunitylabdhub.core.models.entities.Function;

public interface FunctionRepository extends JpaRepository<Function, String> {

        List<Function> findByProject(String project);

        Page<Function> findAll(Pageable pageable);

        @Query("SELECT a FROM Function a WHERE (a.name, a.created) IN " +
                        "(SELECT a2.name, MAX(a2.created) FROM Function a2 GROUP BY a2.name) "
                        +
                        "ORDER BY a.created DESC")
        List<Function> findAllLatestFunctions();

        ////////////////////////////
        // CONTEXT SPECIFIC QUERY //
        ////////////////////////////

        Page<Function> findAllByProjectAndNameOrderByCreatedDesc(String project, String name, Pageable pageable);

        @Query("SELECT a FROM Function a WHERE a.project = :project AND (a.name, a.project, a.created) IN " +
                        "(SELECT a2.name, a2.project, MAX(a2.created) FROM Function a2 WHERE a2.project = :project GROUP BY a2.name, a2.project) "
                        +
                        "ORDER BY a.created DESC")
        Page<Function> findAllLatestFunctionsByProject(@Param("project") String project, Pageable pageable);

        Optional<Function> findByProjectAndNameAndId(@Param("project") String project, @Param("name") String name,
                        @Param("id") String id);

        @Query("SELECT a FROM Function a WHERE a.project = :project AND a.name = :name " +
                        "AND a.created = (SELECT MAX(a2.created) FROM Function a2 WHERE a2.project = :project AND a2.name = :name)")
        Optional<Function> findLatestFunctionByProjectAndName(@Param("project") String project,
                        @Param("name") String name);

        @Query("SELECT a FROM Function a WHERE a.project = :project AND a.id = :id " +
                        "AND a.created = (SELECT MAX(a2.created) FROM Function a2 WHERE a2.project = :project AND a2.id = :id)")
        Optional<Function> findLatestFunctionByProjectAndId(@Param("project") String project,
                        @Param("id") String id);

        boolean existsByProjectAndNameAndId(String project, String name, String id);

        @Modifying
        @Query("DELETE FROM Function a WHERE a.project = :project AND a.name = :name AND a.id = :id")
        void deleteByProjectAndNameAndId(@Param("project") String project, @Param("name") String name,
                        @Param("id") String id);

        boolean existsByProjectAndName(String project, String name);

        @Modifying
        @Query("DELETE FROM Function a WHERE a.project = :project AND a.name = :name ")
        void deleteByProjectAndName(@Param("project") String project, @Param("name") String name);

        @Modifying
        @Query("DELETE FROM Function a WHERE a.project = :project ")
        void deleteByProjectName(@Param("project") String project);
}
