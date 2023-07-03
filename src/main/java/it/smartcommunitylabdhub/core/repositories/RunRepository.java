package it.smartcommunitylabdhub.core.repositories;

import org.springframework.data.jpa.repository.JpaRepository;

import it.smartcommunitylabdhub.core.models.entities.Run;

import java.util.List;

public interface RunRepository extends JpaRepository<Run, String> {

    List<Run> findByProject(String uuid);

    List<Run> findByTask(String task);
}
