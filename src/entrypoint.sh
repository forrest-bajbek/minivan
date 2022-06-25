#!/bin/sh

echo "Waiting for Redis..."

# while ! nc -z minivan-db 6379; do
#   sleep 0.1
# done

echo "Redis started"

exec "$@"
