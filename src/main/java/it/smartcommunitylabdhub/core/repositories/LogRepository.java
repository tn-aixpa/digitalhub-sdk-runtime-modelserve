package it.smartcommunitylabdhub.core.repositories;

import org.springframework.data.jpa.repository.JpaRepository;

import it.smartcommunitylabdhub.core.models.entities.Log;

import java.util.List;

public interface LogRepository extends JpaRepository<Log, String> {

    List<Log> findByProject(String name);

    List<Log> findByRun(String uuid);
}
