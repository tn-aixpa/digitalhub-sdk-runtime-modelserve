package it.smartcommunitylabdhub.dbt.components.runnables.events.publishers;

import org.springframework.context.ApplicationEventPublisher;

import it.smartcommunitylabdhub.core.annotations.RunPublisherComponent;
import it.smartcommunitylabdhub.core.components.kinds.factory.publishers.KindPublisher;
import it.smartcommunitylabdhub.core.models.dtos.RunDTO;
import it.smartcommunitylabdhub.dbt.components.runnables.events.messages.DbtMessage;

/**
 * DbtEventPublisher.java
 *
 * This class is responsible for publishing Dbt (Data Build Tool) events using Spring Application
 * Event mechanism.
 *
 */
@RunPublisherComponent(platform = "dbt", perform = "build")
public class DbtEventPublisher implements KindPublisher<RunDTO, Void> {

    private final ApplicationEventPublisher applicationEventPublisher;

    /**
     * Constructor to initialize the ApplicationEventPublisher.
     *
     * @param applicationEventPublisher The Spring ApplicationEventPublisher.
     */
    public DbtEventPublisher(ApplicationEventPublisher applicationEventPublisher) {
        this.applicationEventPublisher = applicationEventPublisher;
    }

    /**
     * Publish a Dbt event with the provided RunDTO object.
     *
     * @param runDTO The RunDTO object to include in the event.
     * @return Null since this method is designed for void return.
     */
    @Override
    public Void publish(RunDTO runDTO) {
        // produce event with the runDTO object
        DbtMessage dbtMessage = new DbtMessage(runDTO);
        applicationEventPublisher.publishEvent(dbtMessage);
        return null;
    }
}
