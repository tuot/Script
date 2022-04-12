#!/bin/bash

set -ex

if [ ! "$HOST" ]; then
    echo "HOST is not set"
    exit 1
fi

DB_NAME=bundleb2b-v2.0
IP_DB_NAME=invoice-portal

DB_USER=postgres
DB_PASSWORD=password
DB_PORT=5433

MYDB="postgresql://${DB_USER}:${DB_PASSWORD}@${HOST}:${DB_PORT}/${DB_NAME}"
IP_DB="postgresql://${DB_USER}:${DB_PASSWORD}@${HOST}:${DB_PORT}/${IP_DB_NAME}"

if [ ! -f "${DB_NAME}.sql" ]; then
    pg_dump --dbname="${MYDB}" -f "${DB_NAME}.sql"
fi
if [ ! -f "${IP_DB_NAME}.sql" ]; then
    pg_dump --dbname="${IP_DB}" -f "${IP_DB_NAME}.sql"
fi

echo "export done"

# drop database
psql -U postgres -c "drop database ""${DB_NAME}"
psql -U postgres -c "drop database ""${IP_DB_NAME}"

# create database
psql -U postgres -c "create database ""${DB_NAME}"
psql -U postgres -c "create database ""${IP_DB_NAME}"

# import
psql -U postgres -d "bundleb2b-v2.0-Dev" -f "${DB_NAME}.sql"
rm "${DB_NAME}.sql"

psql -U postgres -d "invoice-portal" -f "${IP_DB_NAME}.sql"
rm "${IP_DB_NAME}.sql"

echo "import done"
