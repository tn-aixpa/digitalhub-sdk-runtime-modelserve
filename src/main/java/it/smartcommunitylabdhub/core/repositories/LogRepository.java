package it.smartcommunitylabdhub.core.repositories;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Modifying;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import it.smartcommunitylabdhub.core.models.entities.log.Log;
import java.util.List;

public interface LogRepository extends JpaRepository<Log, String> {

    List<Log> findByProject(String name);

    List<Log> findByRun(String uuid);

    @Modifying
    @Query("DELETE FROM Log l WHERE l.project = :project ")
    void deleteByProjectName(@Param("project") String project);
}
