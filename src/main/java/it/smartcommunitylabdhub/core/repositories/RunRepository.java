package it.smartcommunitylabdhub.core.repositories;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Modifying;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import it.smartcommunitylabdhub.core.models.entities.run.Run;
import java.util.List;

public interface RunRepository extends JpaRepository<Run, String> {

    List<Run> findByProject(String uuid);

    List<Run> findByTask(String task);

    @Modifying
    @Query("DELETE FROM Run r WHERE r.project = :project ")
    void deleteByProjectName(@Param("project") String project);
}
