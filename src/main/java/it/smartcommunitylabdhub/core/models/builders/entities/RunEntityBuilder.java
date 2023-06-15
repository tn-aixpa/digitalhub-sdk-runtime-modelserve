package it.smartcommunitylabdhub.core.models.builders.entities;

import java.util.Date;

import org.hibernate.annotations.CreationTimestamp;
import org.hibernate.annotations.UpdateTimestamp;

import it.smartcommunitylabdhub.core.models.builders.EntityFactory;
import it.smartcommunitylabdhub.core.models.converters.ConversionUtils;
import it.smartcommunitylabdhub.core.models.dtos.RunDTO;
import it.smartcommunitylabdhub.core.models.entities.Run;
import it.smartcommunitylabdhub.core.models.enums.State;
import jakarta.persistence.Column;
import jakarta.persistence.EnumType;
import jakarta.persistence.Enumerated;
import jakarta.persistence.Id;
import jakarta.persistence.Lob;

public class RunEntityBuilder {

        private RunDTO runDTO;

        public RunEntityBuilder(
                        RunDTO RunDTO) {
                this.runDTO = RunDTO;
        }

}

/*
 * 
 * 
 * @Id
 * private String id;
 * 
 * @Column(nullable = false)
 * private String project;
 * 
 * @Column(nullable = false)
 * private String name;
 * 
 * @Column(nullable = false)
 * private String type;
 * 
 * @Lob
 * private byte[] body;
 * 
 * @CreationTimestamp
 * 
 * @Column(updatable = false)
 * private Date created;
 * 
 * @UpdateTimestamp
 * private Date updated;
 * 
 * @Enumerated(EnumType.STRING)
 * private State state;
 * 
 */