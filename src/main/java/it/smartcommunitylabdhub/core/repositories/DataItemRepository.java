package it.smartcommunitylabdhub.core.repositories;

import java.util.List;

import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;

import it.smartcommunitylabdhub.core.models.entities.DataItem;

public interface DataItemRepository extends JpaRepository<DataItem, String> {

    List<DataItem> findByProject(String project);

    Page<DataItem> findAll(Pageable pageable);
}
