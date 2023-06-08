package it.smartcommunitylabdhub.core.models.accessors.kinds.interfaces;

import java.util.Date;

import it.smartcommunitylabdhub.core.models.converters.ConversionUtils;

public interface ProjectFieldAccessor extends CommonFieldAccessor {

    default String getName() {
        return mapHasField(getMetadata(), "name") ? (String) getMetadata().get("name") : null;
    }

    default Date getCreated() {
        return mapHasField(getMetadata(), "created") ? ConversionUtils.convert(
                getMetadata().get("created"), "datetime") : null;
    }
}
