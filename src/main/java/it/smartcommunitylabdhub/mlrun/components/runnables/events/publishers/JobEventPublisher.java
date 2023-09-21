package it.smartcommunitylabdhub.mlrun.components.runnables.events.publishers;

import org.springframework.context.ApplicationEventPublisher;

import it.smartcommunitylabdhub.core.annotations.RunPublisherComponent;
import it.smartcommunitylabdhub.core.components.kinds.factory.publishers.KindPublisher;
import it.smartcommunitylabdhub.core.models.dtos.RunDTO;
import it.smartcommunitylabdhub.mlrun.components.runnables.events.messages.JobMessage;

@RunPublisherComponent(platform = "job", perform = "build")
public class JobEventPublisher implements KindPublisher<RunDTO, Void> {

    private final ApplicationEventPublisher applicationEventPublisher;

    public JobEventPublisher(ApplicationEventPublisher applicationEventPublisher) {
        this.applicationEventPublisher = applicationEventPublisher;
    }

    @Override
    public Void publish(RunDTO runDTO) {
        // produce event with the runDTO object
        JobMessage jobMessage = new JobMessage(runDTO);
        applicationEventPublisher.publishEvent(jobMessage);
        return null;
    }

}
