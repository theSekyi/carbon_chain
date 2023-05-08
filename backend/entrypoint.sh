#!/bin/sh

# This script waits for PostgreSQL to start, then executes the given command.

# PostgreSQL service configuration
postgres_host="web-db"
postgres_port="5432"

echo "Waiting for PostgreSQL at ${postgres_host}:${postgres_port}..."

while ! nc -z "${postgres_host}" "${postgres_port}"; do
  sleep 0.1
done

echo "PostgreSQL started"

# Execute the given command
exec "$@"
