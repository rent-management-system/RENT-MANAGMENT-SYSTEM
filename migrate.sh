#!/bin/bash

# This script is intended to be run from the root of the project directory.

# Uninstall conflicting driver
./Bate/bin/pip uninstall -y psycopg2-binary

# Install dependencies
./Bate/bin/pip install -r backend/user_service/requirements.txt



# Upgrade to the latest revision
./Bate/bin/alembic -c backend/user_service/alembic.ini upgrade head

echo "Database migration script executed successfully."
