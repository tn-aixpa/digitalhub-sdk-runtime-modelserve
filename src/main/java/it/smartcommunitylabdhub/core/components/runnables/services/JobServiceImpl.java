package it.smartcommunitylabdhub.core.components.runnables.services;

import org.springframework.stereotype.Service;

import it.smartcommunitylabdhub.core.components.runnables.dispatcher.MessageDispatcher;
import it.smartcommunitylabdhub.core.components.runnables.services.interfaces.JobService;
import it.smartcommunitylabdhub.core.models.dtos.RunDTO;
import jakarta.transaction.Transactional;

@Service
public class JobServiceImpl implements JobService {

    private final MessageDispatcher messageDispatcher;

    public JobServiceImpl(MessageDispatcher messageDispatcher) {
        this.messageDispatcher = messageDispatcher;
    }

    @Override
    @Transactional
    public void run(RunDTO runDTO) {
        // TODO Auto-generated method stub
        System.out.println("1. Call api to get run status");
        System.out.println("2. Dispatch event to event BUS");
    }

}
