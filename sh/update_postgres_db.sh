#!/bin/bash

set -ex

if [ ! "$HOST" ]; then
    echo "HOST is not set"
    exit 1
fi

DB_NAME=bundleb2b-v2.0
IP_DB_NAME=invoice-portal

MYDB="postgresql://postgres:password@${HOST}:5433/${DB_NAME}"
IP_DB="postgresql://postgres:password@${HOST}:5433/${IP_DB_NAME}"

if [ ! -f "db.sql" ]; then
    pg_dump --dbname="${MYDB}" -f db.sql
fi
if [ ! -f "ip_db.sql" ]; then
    pg_dump --dbname="${IP_DB}" -f ip_db.sql
fi

echo "export done"

# drop database
psql -U postgres -c "drop database ""${DB_NAME}"
psql -U postgres -c "drop database ""${IP_DB_NAME}"

# create database
psql -U postgres -c "create database ""${DB_NAME}"
psql -U postgres -c "create database ""${IP_DB_NAME}"

# import
psql -U postgres -d "bundleb2b-v2.0-Dev" -f db.sql
psql -U postgres -d "invoice-portal" -f ip_db.sql

rm db.sql ip_db.sql
echo "import done"
