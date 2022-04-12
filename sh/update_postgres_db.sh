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

DB_LIST="${DB_NAME} ${IP_DB_NAME}"

start=$(date "+%s")
for name in $DB_LIST; do
    {
        if [ ! -f "${name}.sql" ]; then
            DB_URL="postgresql://${DB_USER}:${DB_PASSWORD}@${HOST}:${DB_PORT}/${name}"
            pg_dump --dbname="${DB_URL}" -f "${name}.sql"
        fi

        psql -U postgres -c "drop database IF EXISTS \"${name}\""
        psql -U postgres -c "create database \"${name}\""
        psql -U postgres -d "${name}" -f "${name}.sql"
        rm "${name}.sql"
    } &
done
wait
end=$(date "+%s")
echo "It takes $((end - start)) seconds to complete this task..."
