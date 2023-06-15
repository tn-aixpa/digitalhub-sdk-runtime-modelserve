package it.smartcommunitylabdhub.core.repositories;

import org.springframework.data.jpa.repository.JpaRepository;

import it.smartcommunitylabdhub.core.models.entities.Task;

public interface TaskRepository extends JpaRepository<Task, String> {

}
