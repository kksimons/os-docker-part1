#!/bin/bash

# Start PostgreSQL service
echo "Initializing PostgreSQL..."
service postgresql start

# Wait for PostgreSQL to be ready
echo "Waiting for PostgreSQL to be ready..."
until pg_isready -h localhost -p 5432; do
  echo "PostgreSQL is not ready yet. Retrying in 5 seconds..."
  sleep 5
done
echo "PostgreSQL is ready."

# Verify PostgreSQL connection
echo "Verifying PostgreSQL connection..."
if ! su postgres -c "psql -U postgres -c '\l'" > /dev/null 2>&1; then
  echo "PostgreSQL connection failed. Exiting."
  exit 1
fi
echo "PostgreSQL connection successful."

# Create PostgreSQL user if it doesn't exist
echo "Checking if user '${POSTGRES_USER}' exists..."
if ! su postgres -c "psql -tc \"SELECT 1 FROM pg_roles WHERE rolname='${POSTGRES_USER}'\" | grep -q 1"; then
  echo "Creating user '${POSTGRES_USER}'..."
  su postgres -c "psql -c \"CREATE USER \\\"${POSTGRES_USER}\\\" WITH PASSWORD '${POSTGRES_PASSWORD}';\""
else
  echo "User '${POSTGRES_USER}' already exists."
fi

# Set the password for the user
echo "Setting password for user '${POSTGRES_USER}'..."
su postgres -c "psql -c \"ALTER USER \\\"${POSTGRES_USER}\\\" WITH PASSWORD '${POSTGRES_PASSWORD}';\""

# Create the database if it doesn't exist
echo "Checking if database '${POSTGRES_DB}' exists..."
if ! su postgres -c "psql -tc \"SELECT 1 FROM pg_database WHERE datname = '${POSTGRES_DB}'\" | grep -q 1"; then
  echo "Creating database '${POSTGRES_DB}'..."
  if su postgres -c "createdb -U postgres ${POSTGRES_DB}"; then
    echo "Database '${POSTGRES_DB}' created successfully."
  else
    echo "Failed to create database '${POSTGRES_DB}'. Exiting."
    exit 1
  fi
else
  echo "Database '${POSTGRES_DB}' already exists."
fi

# Validate database creation
echo "Validating database '${POSTGRES_DB}'..."
if ! su postgres -c "psql -tc \"SELECT 1 FROM pg_database WHERE datname = '${POSTGRES_DB}'\" | grep -q 1"; then
  echo "Database validation failed. Exiting."
  exit 1
fi
echo "Database '${POSTGRES_DB}' is valid."

# Run the initialization SQL script if provided
if [ -f /app/db-init/init.sql ]; then
  echo "Found initialization SQL script. Running it..."
  if su postgres -c "psql -U postgres -d \"${POSTGRES_DB}\" -f /app/db-init/init.sql"; then
    echo "Initialization SQL script executed successfully."
  else
    echo "Failed to execute initialization SQL script. Exiting."
    exit 1
  fi
else
  echo "No initialization SQL script found. Skipping."
fi

# Grant privileges to the user for the new database
echo "Granting privileges on database '${POSTGRES_DB}' to user '${POSTGRES_USER}'..."
su postgres -c "psql -U postgres -c \"GRANT ALL PRIVILEGES ON DATABASE \\\"${POSTGRES_DB}\\\" TO \\\"${POSTGRES_USER}\\\"\""

# Change ownership of the public schema to the user
echo "Changing ownership of schema 'public' to user '${POSTGRES_USER}'..."
su postgres -c "psql -U postgres -d ${POSTGRES_DB} -c \"ALTER SCHEMA public OWNER TO \\\"${POSTGRES_USER}\\\"\""

# Grant privileges on schema objects to the user
echo "Granting privileges on schema objects to user '${POSTGRES_USER}'..."
su postgres -c "psql -U postgres -d ${POSTGRES_DB} -c \"GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO \\\"${POSTGRES_USER}\\\"\""
su postgres -c "psql -U postgres -d ${POSTGRES_DB} -c \"GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO \\\"${POSTGRES_USER}\\\"\""
su postgres -c "psql -U postgres -d ${POSTGRES_DB} -c \"GRANT ALL PRIVILEGES ON ALL FUNCTIONS IN SCHEMA public TO \\\"${POSTGRES_USER}\\\"\""

# Start the FastAPI app
echo "Starting FastAPI app..."
uvicorn app.app:app --host 0.0.0.0 --port 8080 --reload &

# Start the Streamlit app
echo "Starting Streamlit app..."
streamlit run app/streamlit_app.py --server.port=8501 --server.address=0.0.0.0 &

# Keep the script running
echo "All services started successfully. Keeping container alive."
tail -f /dev/null
