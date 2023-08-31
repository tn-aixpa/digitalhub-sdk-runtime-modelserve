# Python Script Documentation

## Overview

This Python script is designed to interact with a DataHub Core backend and a dbt (data build tool) project. It performs the following tasks:

1. Retrieves run information from DataHub Core.
2. Initializes a dbt project based on the run specification.
3. Runs dbt models.
4. Extracts relevant information from dbt execution results.
5. Creates and updates dataitems in DataHub Core based on the dbt results.

## Script Components

### Dependencies

The script requires the following Python packages:

- `subprocess`: For running external processes.
- `os`: For interacting with the operating system.
- `json`: For working with JSON data.
- `base64`: For encoding and decoding data as base64.
- `requests`: For making HTTP requests.
- `sys`: For interacting with the Python runtime environment.
- `re`: For working with regular expressions.
- `dbt.cli.main`: To access dbt CLI functionality.
- `datetime.datetime`: For handling date and time values.
- `enum.Enum`: For defining enumerated types.

### Functions

#### `CustomJSONEncoder`

A custom JSON encoder class that extends `json.JSONEncoder`. It handles the serialization of specific types such as `Enum` and `datetime` objects.

#### `make_post_request(base_url, endpoint, data=None)`

Makes a POST request to a specified endpoint on a given base URL with optional JSON data.

#### `make_get_request(base_url, endpoint, *path_params)`

Makes a GET request to a specified endpoint on a given base URL with optional path parameters.

#### `make_put_request(base_url, endpoint, data=None, *path_params)`

Makes a PUT request to a specified endpoint on a given base URL with optional JSON data and path parameters.

#### `get_run()`

Retrieves run information from DataHub Core by making a GET request to the appropriate endpoint.

#### `create_dataitem(data: dict)`

Creates a dataitem in DataHub Core by making a POST request with the provided data.

#### `update_run(run_id: str, run: dict)`

Updates a run in DataHub Core by making a PUT request with the updated run data.

#### `parse_dbt_url(url)`

Parses a dbt URL using a regular expression pattern and extracts components like project, function, and version.

#### `initialize_project(run: dict)`

Initializes a dbt project by creating necessary configuration files and directories based on the provided run specification.

#### `extract_response(res)`

Extracts relevant information from a dbt execution result, transforming it into a dictionary format.

#### `main()`

The main function orchestrates the entire process. It retrieves run information, initializes the dbt project, runs dbt models, processes the results, and updates DataHub Core accordingly.

## Usage

1. Ensure you have the required Python packages installed. You can use the following command to install them:

   ```
   pip install requests dbt
   ```

2. Set environment variables `DHUB_CORE_ENDPOINT`, `RUN_ID`, `POSTGRES_DB_HOST`, `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_PORT`, and `POSTGRES_DB` appropriately.

3. Run the script. It will perform the following steps:
   - Retrieve run information from DataHub Core.
   - Initialize a dbt project based on the run specification.
   - Run dbt models.
   - Process and extract information from the dbt execution results.
   - Create or update dataitems in DataHub Core.

Note: The script may require additional configuration and adjustments based on your specific setup and requirements.

## Disclaimer

This documentation provides an overview of the provided Python script. It is recommended to review and test the script in your environment before deploying it to a production setting. Make sure to adapt the script to your specific needs, configuration, and security considerations.
