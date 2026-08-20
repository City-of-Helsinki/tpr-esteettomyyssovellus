CREATE USER esteettomyyslomake;
ALTER USER esteettomyyslomake WITH PASSWORD 'esteettomyyslomake123';
CREATE DATABASE esteettomyyslomake;
GRANT ALL PRIVILEGES ON DATABASE esteettomyyslomake TO esteettomyyslomake;

-- The following is only for local dev. In test/prod the database is a remote
-- managed instance and this file (along with the db service in docker-compose)
-- is not used.
\c esteettomyyslomake

-- Required by audit triggers
CREATE EXTENSION IF NOT EXISTS hstore;

-- Schema used by Django (SEARCH_PATH=ar_test,public in local_dev/.env)
CREATE SCHEMA IF NOT EXISTS ar_test;
GRANT ALL ON SCHEMA ar_test TO esteettomyyslomake;

-- Audit schema – required by audit triggers attached to ar_test tables
CREATE SCHEMA IF NOT EXISTS audit;
GRANT USAGE ON SCHEMA audit TO esteettomyyslomake;

CREATE SEQUENCE IF NOT EXISTS audit.logged_actions_event_id_seq;

CREATE TABLE IF NOT EXISTS audit.logged_actions (
    event_id          bigint DEFAULT nextval('audit.logged_actions_event_id_seq') NOT NULL,
    schema_name       text NOT NULL,
    table_name        text NOT NULL,
    relid             oid NOT NULL,
    session_user_name text,
    action_tstamp_tx  timestamp with time zone NOT NULL,
    action_tstamp_stm timestamp with time zone NOT NULL,
    action_tstamp_clk timestamp with time zone NOT NULL,
    transaction_id    bigint,
    application_name  text,
    client_addr       inet,
    client_port       integer,
    client_query      text,
    action            text NOT NULL,
    row_data          hstore,
    changed_fields    hstore,
    statement_only    boolean NOT NULL,
    CONSTRAINT logged_actions_action_check CHECK (action IN ('I','D','U','T'))
);

GRANT ALL ON audit.logged_actions TO esteettomyyslomake;
GRANT USAGE, UPDATE ON SEQUENCE audit.logged_actions_event_id_seq TO esteettomyyslomake;
ALTER USER esteettomyyslomake WITH SUPERUSER;