#!/bin/bash

# Create a new system user without password
adduser --disabled-password --gecos "" dbt

# Set the new user as predefined
chown -R dbt: /digitalhub-core