#!/bin/bash

set -eu

DB_NAME=bundleb2b-v2.0
IP_DB_NAME=invoice-portal

ACTION=$1
DB_USER=postgres
DB_LIST="$DB_NAME $IP_DB_NAME"

if [ "$ACTION" = "backup" ]; then
    if [ "$#" -ne 4 ]; then
        echo "Please input database Host, Port and Password" >&2
        exit 1
    fi
    HOST=$2
    DB_PORT=$3
    DB_PASSWORD=$4
fi


start=$(date "+%s")
if [ "$ACTION" = "backup" ]; then
    for name in $DB_LIST; do
        {
            db_dump_file="$name.dump"
            if [ ! -f "$db_dump_file" ]; then
                DB_URL="postgresql://$DB_USER:$DB_PASSWORD@$HOST:$DB_PORT/$name"
                set -x
                # pg_dump --dbname="$DB_URL" -f "$db_dump_file"
                pg_dump --format=custom --dbname="$DB_URL" -f "$db_dump_file"
                set +x
            fi
        } &
    done
    wait
elif [ "$ACTION" = "restore" ]; then
    for name in $DB_LIST; do
        {
            db_dump_file="$name.dump"
            psql -U postgres -c "drop database IF EXISTS \"$name\""
            psql -U postgres -c "create database \"$name\""
            # psql -U postgres -d "$name" -f "$db_dump_file" 
            pg_restore -U postgres -v --format=custom -d "$name" "$db_dump_file"
            rm "$db_dump_file"
        } &
    done
    wait
fi

end=$(date "+%s")
echo "It takes $((end - start)) seconds to complete this task..."
