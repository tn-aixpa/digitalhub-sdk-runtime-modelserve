package it.smartcommunitylabdhub.core.models.accessors.utils;

import java.util.regex.Matcher;
import java.util.regex.Pattern;

import org.springframework.http.HttpStatus;

import it.smartcommunitylabdhub.core.exceptions.CoreException;
import it.smartcommunitylabdhub.core.models.entities.function.FunctionDTO;
import it.smartcommunitylabdhub.core.models.entities.workflow.WorkflowDTO;
import it.smartcommunitylabdhub.core.models.interfaces.BaseEntity;

public class TaskUtils {

	private static final Pattern TASK_PATTERN = Pattern.compile("([^:/]+)://([^/]+)/([^:]+):(.+)");

	private TaskUtils() {}

	public static TaskAccessor parseTask(String taskString) {
		Matcher matcher = TASK_PATTERN.matcher(taskString);
		if (matcher.matches()) {
			String kind = matcher.group(1);
			String project = matcher.group(2);
			String function = matcher.group(3);
			String version = matcher.group(4);

			return new TaskAccessor(kind, project, function, version);
		}
		throw new CoreException("InvalidTaskStringCase",
				"Cannot create accessor for the given task string.",
				HttpStatus.INTERNAL_SERVER_ERROR);
	}

	public static <T extends BaseEntity> String buildTaskString(T type) {
		if (type instanceof FunctionDTO) {

			FunctionDTO f = (FunctionDTO) type;
			return f.getKind() + "://" + f.getProject() + "/" + f.getName() + ":" + f.getId();
		} else if (type instanceof WorkflowDTO) {

			WorkflowDTO w = (WorkflowDTO) type;
			return w.getKind() + "://" + w.getProject() + "/" + w.getName() + ":" + w.getId();
		} else {
			throw new CoreException("CannotComposeTaskField",
					"Cannot compose task field for the given object.",
					HttpStatus.INTERNAL_SERVER_ERROR);
		}

	}
}
