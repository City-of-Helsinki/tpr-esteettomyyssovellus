#!/bin/sh

set -eu

# init_db.sql creates the target database and the supporting audit objects
# before this script is run by the PostgreSQL image entrypoint. --clean makes
# the restore replace those overlapping objects with the versions in the dump.
pg_restore \
    --dbname=esteettomyyslomake \
    --clean \
    --if-exists \
    --no-owner \
    --exit-on-error \
    /docker-entrypoint-initdb.d/dump.backup
