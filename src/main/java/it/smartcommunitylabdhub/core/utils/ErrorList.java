package it.smartcommunitylabdhub.core.utils;

public enum ErrorList {
	INTERNAL_SERVER_ERROR("InternalServerError", "Internal Server Error"),

	/** FUNCTION */
	FUNCTION_NOT_FOUND("FunctionNotFound", "The function you are searching for does not exist."),
	/** */
	FUNCTION_NOT_MATCH("FunctionNotMatch",
			"Trying to update a function with an uuid different from the one passed in the request."),
	/**  */
	DUPLICATE_FUNCTION("DuplicateFunction", "Cannot create function."),

	/** PROJECT */
	PROJECT_NOT_FOUND("ProjectNotFound", "The project you are searching for does not exist."),
	/** */
	PROJECT_NOT_MATCH("ProjectNotMatch",
			"Trying to update a project with a UUID different from the one passed in the request."),
	/** */
	DUPLICATE_PROJECT("DuplicateProjectIdOrName",
			"Cannot create the project, duplicated Id or Name");


	private final String value;
	private final String reason;

	ErrorList(String value, String reason) {
		this.value = value;
		this.reason = reason;
	}

	public String getValue() {
		return value;
	}

	public String getReason() {
		return reason;
	}
}
