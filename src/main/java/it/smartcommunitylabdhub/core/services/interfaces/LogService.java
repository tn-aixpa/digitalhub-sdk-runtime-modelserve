package it.smartcommunitylabdhub.core.services.interfaces;

import java.util.List;

import org.springframework.data.domain.Pageable;

import it.smartcommunitylabdhub.core.models.dtos.LogDTO;

public interface LogService {

    List<LogDTO> getLogs(Pageable pageable);

    LogDTO getLog(String uuid);

    List<LogDTO> getLogsByRunUuid(String uuid);

    boolean deleteLog(String uuid);

    LogDTO createLog(LogDTO logDTO);

}
