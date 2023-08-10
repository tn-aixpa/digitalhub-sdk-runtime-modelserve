package it.smartcommunitylabdhub.dbt.components.runnables.events.publishers;

import org.springframework.context.ApplicationEventPublisher;

import it.smartcommunitylabdhub.core.annotations.RunPublisherComponent;
import it.smartcommunitylabdhub.core.components.kinds.factory.publishers.KindPublisher;
import it.smartcommunitylabdhub.core.models.dtos.RunDTO;
import it.smartcommunitylabdhub.dbt.components.runnables.events.messages.DbtMessage;

@RunPublisherComponent(type = "dbt")
public class DbtEventPublisher implements KindPublisher<RunDTO, Void> {

    private final ApplicationEventPublisher applicationEventPublisher;

    public DbtEventPublisher(ApplicationEventPublisher applicationEventPublisher) {
        this.applicationEventPublisher = applicationEventPublisher;
    }

    @Override
    public Void publish(RunDTO runDTO) {
        // produce event with the runDTO object
        DbtMessage dbtMessage = new DbtMessage(runDTO);
        applicationEventPublisher.publishEvent(dbtMessage);
        return null;
    }

}
