-- Connect to PostgreSQL server as a superuser
\c postgres;

-- Create a new database
CREATE DATABASE pdsa;

-- Create a new user with a password
CREATE USER pdsa WITH ENCRYPTED PASSWORD 'change_when_running';

-- Grant all privileges on the new database to the new user
GRANT ALL PRIVILEGES ON DATABASE pdsa TO pdsa;

