package it.smartcommunitylabdhub.core.components.kubernetes;

import io.fabric8.kubernetes.api.model.Event;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Component;

import java.util.regex.Matcher;
import java.util.regex.Pattern;

@Component
@Slf4j
public class EventLogger {

    public void logEvent(Event event, String jobName) {

        // Parse job name : is composed by "<job>-<kind>-<runId>"
        String pattern = "(?<type>\\w+)-(?<kind>\\w+)-(?<runId>[a-fA-F0-9-]+)";


        Pattern regex = Pattern.compile(pattern);
        Matcher matcher = regex.matcher(jobName);

        if (matcher.matches()) {
            String type = matcher.group("type");
            String kind = matcher.group("kind");
            String runId = matcher.group("runId");

            System.out.println("Type: " + type);
            System.out.println("Kind: " + kind);
            System.out.println("Run ID (UUID4): " + runId);

        } else {
            log.error("Cannot parse job name from kubernetes events: expected format \"<type>-<kind>-<runId>\", received: "
                    + jobName);
        }


        // ObjectMapper objectMapper = new ObjectMapper();

        // try {
        // String eventJson = objectMapper.writeValueAsString(event);
        // System.out.println("Event JSON:\n" + eventJson);
        // } catch (JsonProcessingException e) {
        // e.printStackTrace();
        // }

    }
}
