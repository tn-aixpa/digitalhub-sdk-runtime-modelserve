package it.smartcommunitylabdhub.core.utils;

public enum ErrorList {
	INTERNAL_SERVER_ERROR("InternalServerError", "Internal Server Error"),
	/** */
	FUNCTION_NOT_FOUND("FunctionNotFound", "The function you are searching for does not exist."),
	/** */
	FUNCTION_NOT_MATCH("FunctionNotMatch",
			"Trying to update a function with an uuid different from the one passed in the request."),
	/**  */
	DUPLICATE_FUNCTION("DuplicateFunction", "Cannot create function.");

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
