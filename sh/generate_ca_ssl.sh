#!/bin/bash

set -eu

export MSYS_NO_PATHCONV=1

# check if enter file name and common name
if [ $# -ne 2 ]; then
    echo "Usage: $0 <file name> <common name>"
    exit 1
fi

FILE_NAME="${1}"
COMMON_NAME="${2}"

openssl req -out "${FILE_NAME}"_ca.pem -new -x509 -nodes -days 3650 \
    -subj "/C=/ST=/L=/O=/OU=/CN=${COMMON_NAME}/emailAddress="
mv privkey.pem "${FILE_NAME}"_privkey.pem

echo "00" > "${FILE_NAME}"_index.txt
openssl genrsa -out "${FILE_NAME}".key 2048
openssl req -key "${FILE_NAME}".key -new -out "${FILE_NAME}".req \
    -subj "/C=/ST=/L=/O=/OU=/CN=${COMMON_NAME}App/emailAddress="
openssl x509 -req -in "${FILE_NAME}".req -CA "${FILE_NAME}"_ca.pem -CAkey "${FILE_NAME}"_privkey.pem -CAserial "${FILE_NAME}"_index.txt -out "${FILE_NAME}".pem -days 3650