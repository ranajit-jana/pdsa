-- Connect to PostgreSQL server as a superuser
\c postgres;

-- Create a new database
CREATE DATABASE pdsa;

-- Create a new user with a password
CREATE USER pdsa_admin WITH ENCRYPTED PASSWORD 'change_when_running';

-- Grant all privileges on the new database to the new user
GRANT ALL PRIVILEGES ON DATABASE pdsa TO pdsa_admin;


-- create a user with read and write previledges


-- Create a read-only user
CREATE USER pdsa_read WITH ENCRYPTED PASSWORD 'change_readonly_password';

-- Create a read-write user
CREATE USER pdsa_rw WITH ENCRYPTED PASSWORD 'change_readwrite_password';

-- Grant CONNECT privilege on the database to readonly_user and readwrite_user
GRANT CONNECT ON DATABASE sample_db TO pdsa_read, pdsa_rw;




-- Grant read-only privileges to readonly_user
GRANT USAGE ON SCHEMA public TO pdsa_read;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO pdsa_read;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO pdsa_read;

-- Grant read-write privileges to readwrite_user
GRANT USAGE ON SCHEMA public TO pdsa_rw;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO pdsa_rw;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO pdsa_rw;


-- Connect to the new database
\c pdsa;


-- Create the pii_category table
CREATE TABLE pii_category (
    pii_category_id SERIAL PRIMARY KEY,
    pii_category_name VARCHAR(10) NOT NULL,
     pii_category_description VARCHAR(10) NOT NULL

);
-- Create a sample table
CREATE TABLE pii_entity (
    pii_entity_id SERIAL PRIMARY KEY,
    pii_entity_code VARCHAR(100) NOT NULL,
    pii_entity_description VARCHAR(100) NOT NULL,
    pii_category_id INT REFERENCES pii_category(pii_category_id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

);
