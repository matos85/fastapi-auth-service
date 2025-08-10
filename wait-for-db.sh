#!/bin/sh

host="$1"
shift

# Используем параметры из .env или стандартные
PG_USER=${POSTGRES_USER:-user}
PG_PASSWORD=${POSTGRES_PASSWORD:-password}
PG_DB=${POSTGRES_DB:-auth_db}

until PGPASSWORD=$PG_PASSWORD psql -h "$host" -U "$PG_USER" -d "$PG_DB" -c '\q'; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 1
done

>&2 echo "Postgres is up - executing command"
exec "$@"