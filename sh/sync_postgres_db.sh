#!/bin/bash

set -eu

DB_NAME=bundleb2b-v2.0
IP_DB_NAME=invoice-portal

if [ "$#" -ne 2 ]; then
    echo "Please input database Host and Password" >&2
    exit 1
fi

HOST=$1
DB_USER=postgres
DB_PASSWORD=$2
DB_PORT=5433

DB_LIST="${DB_NAME} ${IP_DB_NAME}"

start=$(date "+%s")
for name in $DB_LIST; do
    {
        if [ ! -f "${name}.sql" ]; then
            DB_URL="postgresql://${DB_USER}:${DB_PASSWORD}@${HOST}:${DB_PORT}/${name}"
            set -x
            pg_dump --dbname="${DB_URL}" -f "${name}.sql"
            set +x
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
