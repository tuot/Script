#!/bin/bash

set -eu

export MSYS_NO_PATHCONV=1

# check if enter file name and common name
if [ $# -ne 1 ]; then
    echo "Usage: $0 <app name>"
    exit 1
fi

APP_NAME="${1}"
DAYS=3650

CA_KEY=CA.key
CA_CERT=CA.cert

CA_INDEX=serial

APP_KEY="${APP_NAME}".key
APP_REQ="${APP_NAME}".req
APP_CERT="${APP_NAME}".cert

echo "00" >${CA_INDEX}

openssl genrsa -out ${CA_KEY} 4096
openssl req -key ${CA_KEY} -out ${CA_CERT} -new -x509 -nodes -days ${DAYS} -subj "/C=/ST=/L=/O=/OU=/CN=${APP_NAME} CA/emailAddress="

openssl genrsa -out "${APP_KEY}" 2048
openssl req -key "${APP_KEY}" -new -out "${APP_REQ}" -subj "/C=/ST=/L=/O=/OU=/CN=${APP_NAME} App/emailAddress="

openssl x509 -req -in "${APP_REQ}" -CA ${CA_CERT} -CAkey ${CA_KEY} -CAserial ${CA_INDEX} -out "${APP_CERT}" -days ${DAYS}
