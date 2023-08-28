package it.smartcommunitylabdhub.core.components.kubernetes;

import java.util.regex.Matcher;
import java.util.regex.Pattern;
import org.springframework.stereotype.Component;
import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import io.fabric8.kubernetes.api.model.Event;
import it.smartcommunitylabdhub.core.utils.RegexList;

@Component
public class EventLogger {

	public void logEvent(Event event) {

		ObjectMapper objectMapper = new ObjectMapper();

		try {
			String eventJson = objectMapper.writeValueAsString(event);
			System.out.println("Event JSON:\n" + eventJson);
		} catch (JsonProcessingException e) {
			e.printStackTrace();
		}

		Pattern pattern = Pattern.compile(RegexList.UUID4_REGEX);
		Matcher matcher = pattern.matcher(event.getMetadata().getName());

		while (matcher.find()) {
			System.out.println("Found UUID: " + matcher.group());
		}
	}
}
