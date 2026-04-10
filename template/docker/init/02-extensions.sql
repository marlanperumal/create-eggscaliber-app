\c {{ project_name | replace('-', '_') }}_dev
CREATE EXTENSION IF NOT EXISTS vector;

\c {{ project_name | replace('-', '_') }}_test
CREATE EXTENSION IF NOT EXISTS vector;

\c {{ project_name | replace('-', '_') }}_migrations_test
CREATE EXTENSION IF NOT EXISTS vector;
