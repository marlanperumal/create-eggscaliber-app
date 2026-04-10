CREATE DATABASE {{ project_name | replace('-', '_') }}_dev;
CREATE DATABASE {{ project_name | replace('-', '_') }}_test;
CREATE DATABASE {{ project_name | replace('-', '_') }}_migrations_test;
