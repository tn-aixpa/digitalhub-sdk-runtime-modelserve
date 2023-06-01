package it.smartcommunitylabdhub.core.services.context;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import it.smartcommunitylabdhub.core.exceptions.CustomException;
import it.smartcommunitylabdhub.core.repositories.ProjectRepository;

@Service
public class ContextService {

    @Autowired
    private ProjectRepository projectRepository;

    public void checkContext(String projectName) throws CustomException {

        this.projectRepository.findByName(projectName)
                .orElseThrow(() -> new CustomException("(Context) Project " + "[" + projectName + "] not found", null));

    }

}
