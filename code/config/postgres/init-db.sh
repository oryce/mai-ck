#!/bin/bash

set -e

psql -v ON_ERROR_STOP=1 -v PSW="'$HIVE_USER_PASSWORD'" <<-'EOSQL'
    CREATE USER hive WITH PASSWORD :PSW;
    CREATE USER keycloak WITH PASSWORD 'keycloak123';
    CREATE DATABASE hive OWNER hive;
    CREATE DATABASE keycloak OWNER keycloak;
EOSQL