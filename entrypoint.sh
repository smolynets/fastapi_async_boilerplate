#!/bin/bash

# Check if Alembic is installed
alembic --version

# Upgrade the database
alembic upgrade head

echo "#############################sdfsfddzfsfdsdzf###########"

# Start the FastAPI application
uvicorn backend.main:app --host 0.0.0.0 --port 8000
