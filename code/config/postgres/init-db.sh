#!/bin/bash

set -e

psql -v ON_ERROR_STOP=1 -v PSW="'$HIVE_USER_PASSWORD'" <<-'EOSQL'
    CREATE USER hive WITH PASSWORD :PSW;
    CREATE DATABASE hive OWNER hive;
EOSQL