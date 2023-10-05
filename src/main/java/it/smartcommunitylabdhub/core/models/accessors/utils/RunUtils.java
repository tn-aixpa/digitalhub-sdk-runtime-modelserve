package it.smartcommunitylabdhub.core.models.accessors.utils;

import java.util.regex.Matcher;
import java.util.regex.Pattern;

import org.springframework.http.HttpStatus;

import it.smartcommunitylabdhub.core.exceptions.CoreException;
import it.smartcommunitylabdhub.core.models.dtos.FunctionDTO;
import it.smartcommunitylabdhub.core.models.dtos.TaskDTO;
import it.smartcommunitylabdhub.core.models.dtos.WorkflowDTO;
import it.smartcommunitylabdhub.core.models.interfaces.BaseEntity;

public class RunUtils {

	private static final Pattern RUN_PATTERN =
			Pattern.compile("([^:/]+)\\+([^+]+)://([^/]+)/([^/]+):(.+)");


	private RunUtils() {}

	public static RunAccessor parseRun(String RunString) {
		Matcher matcher = RUN_PATTERN.matcher(RunString);
		if (matcher.matches()) {
			String kind = matcher.group(1);
			String perform = matcher.group(2);
			String project = matcher.group(3);
			String function = matcher.group(4);
			String version = matcher.group(5);

			return new RunAccessor(kind, perform, project, function, version);
		}
		throw new CoreException("InvalidRunStringCase",
				"Cannot create accessor for the given Run string.",
				HttpStatus.INTERNAL_SERVER_ERROR);
	}

	public static <T extends BaseEntity> String buildRunString(T type, TaskDTO task) {
		if (type instanceof FunctionDTO) {

			FunctionDTO f = (FunctionDTO) type;
			return f.getKind() + "+" + task.getKind() + "://" + f.getProject() + "/"
					+ f.getName() + ":" + f.getId();
		} else if (type instanceof WorkflowDTO) {

			WorkflowDTO w = (WorkflowDTO) type;
			return w.getKind() + "+" + task.getKind() + "://" + w.getProject() + "/"
					+ w.getName() + ":" + w.getId();
		} else {
			throw new CoreException("CannotComposeRunField",
					"Cannot compose Run field for the given object.",
					HttpStatus.INTERNAL_SERVER_ERROR);
		}

	}
}
