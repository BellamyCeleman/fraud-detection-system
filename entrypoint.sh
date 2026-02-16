#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

while ! nc -z postgres 5432; do
  sleep 0.1
done
echo "PostgreSQL started"

while ! nc -z fraud_localstack 4566; do
  sleep 0.5
done
echo "LocalStack started"

if [ "$RUN_MIGRATIONS" = "true" ]; then
  echo "Applying database migrations..."
  /usr/local/bin/uv run alembic upgrade head
fi

echo "Starting: $@"
exec /usr/local/bin/uv run "$@"