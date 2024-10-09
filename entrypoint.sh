#!/bin/bash

# Start PostgreSQL service
echo "Initializing PostgreSQL..."
service postgresql start

# Wait until PostgreSQL is ready
until pg_isready -h localhost -p 5432; do
  echo "Waiting for PostgreSQL to be ready..."
  sleep 2
done

# Create PostgreSQL user if it doesn't exist
su postgres -c "psql -tc \"SELECT 1 FROM pg_roles WHERE rolname='${POSTGRES_USER}'\" | grep -q 1 || psql -c \"CREATE USER \\\"${POSTGRES_USER}\\\" WITH PASSWORD '${POSTGRES_PASSWORD}';\""

# Set the password for the user
su postgres -c "psql -c \"ALTER USER \\\"${POSTGRES_USER}\\\" WITH PASSWORD '${POSTGRES_PASSWORD}';\""

# Create the database if it doesn't exist
su postgres -c "psql -U postgres -tc \"SELECT 1 FROM pg_database WHERE datname = '${POSTGRES_DB}'\" | grep -q 1 || psql -U postgres -c \"CREATE DATABASE ${POSTGRES_DB}\""

# WE NEED TO RUN THIS HERE BEFORE PERMISSIONS
# Run the initialization SQL script, if provided (create tables, etc.)
if [ -f /app/db-init/init.sql ]; then
  echo "Running initialization SQL script..."
  su postgres -c "psql -U postgres -d ${POSTGRES_DB} -f /app/db-init/init.sql"
fi

# Grant privileges to the user for the new database
su postgres -c "psql -U postgres -c \"GRANT ALL PRIVILEGES ON DATABASE ${POSTGRES_DB} TO \\\"${POSTGRES_USER}\\\"\""

# Change ownership of the public schema to the user
su postgres -c "psql -U postgres -d ${POSTGRES_DB} -c \"ALTER SCHEMA public OWNER TO \\\"${POSTGRES_USER}\\\"\""

# Change ownership of all tables in the public schema to the user
su postgres -c "psql -U postgres -d ${POSTGRES_DB} -c \"ALTER TABLE public.students OWNER TO \\\"${POSTGRES_USER}\\\"\""

# Grant privileges to the user on the public schema and its objects
su postgres -c "psql -U postgres -d ${POSTGRES_DB} -c \"GRANT ALL PRIVILEGES ON SCHEMA public TO \\\"${POSTGRES_USER}\\\"\""
su postgres -c "psql -U postgres -d ${POSTGRES_DB} -c \"GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO \\\"${POSTGRES_USER}\\\"\""
su postgres -c "psql -U postgres -d ${POSTGRES_DB} -c \"GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO \\\"${POSTGRES_USER}\\\"\""
su postgres -c "psql -U postgres -d ${POSTGRES_DB} -c \"GRANT ALL PRIVILEGES ON ALL FUNCTIONS IN SCHEMA public TO \\\"${POSTGRES_USER}\\\"\""

# Start the FastAPI app
echo "Starting FastAPI..."
uvicorn app.app:app --host 0.0.0.0 --port 8080 --reload &

# Start the Streamlit app
echo "Starting Streamlit..."
streamlit run app/streamlit_app.py --server.port=8501 --server.address=0.0.0.0

# Keep the script running
exec "$@"
