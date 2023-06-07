package it.smartcommunitylabdhub.core.models.accessors.interfaces;

import java.util.Date;
import java.util.List;
import java.util.Map;

import it.smartcommunitylabdhub.core.models.converters.ConversionUtils;

public interface FunctionFieldAccessor extends CommonFieldAccessor {

    // COMMENT: those below are METADATA function common fields
    // name:String, tag:String, project:String, hash:String, update:Date,
    // labels:Map<String,String>, categories:List<String>

    // HACK: test if this work or not
    @SuppressWarnings("unchecked")
    default Map<String, String> getLabels() {
        return mapHasField(getMetadata(), "labels") ? (Map<String, String>) getMetadata().get("labels") : null;
    }

    @SuppressWarnings("unchecked")
    default List<String> getCategories() {
        return mapHasField(getMetadata(), "categories") ? (List<String>) getMetadata().get("categories") : null;
    }

    default String getName() {
        return mapHasField(getMetadata(), "name") ? (String) getMetadata().get("name") : null;
    }

    default String getTag() {
        return mapHasField(getMetadata(), "tag") ? (String) getMetadata().get("tag") : null;
    }

    default String getProject() {
        return mapHasField(getMetadata(), "project") ? (String) getMetadata().get("project") : null;
    }

    default String getHash() {
        return mapHasField(getMetadata(), "hash") ? (String) getMetadata().get("hash") : null;
    }

    default Date getUpdate() {
        return mapHasField(getMetadata(), "update") ? ConversionUtils.convert(
                getMetadata().get("update"), "datetime") : null;
    }

    // COMMENT: those below are SPEC fuction common fields
    // command:string,
    // args:List<String>????,
    // build: Map<String, Object> -> {..... , commands:List<String>}
    // image:string,
    // description:string ,
    // volumes:List<Map<String, Object>> ->
    // [{name:{'secret':{'secretName':"Username"}}}],
    // volume_mounts:List<Map<String, String>>,
    // env:List<Map<String, String>>

    default String getCommand() {
        return mapHasField(getMetadata(), "command") ? (String) getMetadata().get("command") : null;
    }

    @SuppressWarnings("unchecked")
    default List<String> getArgs() {
        return mapHasField(getMetadata(), "args") ? (List<String>) getMetadata().get("args") : null;
    }

    @SuppressWarnings("unchecked")
    default Map<String, Object> getBuild() {
        return mapHasField(getMetadata(), "build") ? (Map<String, Object>) getMetadata().get("build") : null;
    }

    default String getImage() {
        return mapHasField(getMetadata(), "image") ? (String) getMetadata().get("image") : null;
    }

    default String getDescription() {
        return mapHasField(getMetadata(), "description") ? (String) getMetadata().get("description") : null;
    }

    @SuppressWarnings("unchecked")
    default List<Map<String, Object>> getVolumes() {
        return mapHasField(getMetadata(), "volumes") ? (List<Map<String, Object>>) getMetadata().get("volumes") : null;
    }

    @SuppressWarnings("unchecked")
    default List<Map<String, Object>> getVolumeMounts() {
        return mapHasField(getMetadata(), "volume_mounts")
                ? (List<Map<String, Object>>) getMetadata().get("volume_mounts")
                : null;
    }

    @SuppressWarnings("unchecked")
    default List<Map<String, String>> getEnv() {
        return mapHasField(getMetadata(), "env")
                ? (List<Map<String, String>>) getMetadata().get("env")
                : null;
    }
}
