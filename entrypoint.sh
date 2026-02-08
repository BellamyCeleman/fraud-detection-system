#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

echo "Waiting for postgres..."
while ! nc -z postgres 5432; do
  sleep 0.1
done
echo "PostgreSQL started"

echo "Applying database migrations..."
alembic upgrade head

echo "Starting application..."
exec "$@"