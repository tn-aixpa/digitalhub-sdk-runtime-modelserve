# Code Documentation

## Purpose

This script retrieves a JSON schema from a backend API and uses datamodel-codegen to generate a Pydantic model based on the schema.

## Dependencies

Make sure you have Python 3.9 or higher installed and also `curl` and `pip`.
Install datamodel-codegen using pip:

```shell
pip install datamodel-codegen
```

## API endpoint

Manually update the BASE_API variable in the script to point to the desired backend API endpoint.

1. Locate the BASE_API variable in the script.
2. Update the value of BASE_API to the desired backend API endpoint.

```bash
BASE_API=http://new-backend-url.com/api/v1/schemas
```

## Run the script

Execute the script and input the uppercase DTO and KIND when prompted.

Example:

```bash
./spec_exporter.sh
```

with DTO `FUNCTION` and KIND `DBT`.

In the same directory as the script, you will find the generated model. The main model you should care is the `Model` class in the generated code.
