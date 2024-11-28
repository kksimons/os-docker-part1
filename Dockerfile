# Use Python base image
FROM python:3.9-slim

# Adding image label name for Docker Part 4 Requirements
LABEL image-name="StudentRestfulAPI"

# Install PostgreSQL
# had to add dos2unix for some reason for this part 2 only to run entrypoint...
RUN apt-get update && apt-get install -y postgresql postgresql-contrib dos2unix && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Set environment variables for PostgreSQL
ENV POSTGRES_USER=user
ENV POSTGRES_PASSWORD=password
ENV POSTGRES_DB=StudentDB
ENV PATH="/usr/lib/postgresql/13/bin:$PATH"

# Set working directory
WORKDIR /app

# Copy the requirements.txt file to the container
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire application to the container
COPY . .

# Make sure the PostgreSQL directories have the right permissions
RUN mkdir -p /var/lib/postgresql/data /run/postgresql && \
    chown -R postgres:postgres /var/lib/postgresql /run/postgresql

# Copy entrypoint script and make it executable
COPY entrypoint.sh /usr/local/bin/entrypoint.sh

# Convert line endings of entrypoint.sh to Unix format
RUN dos2unix /usr/local/bin/entrypoint.sh

# Make entrypoint script executable
RUN chmod +x /usr/local/bin/entrypoint.sh

# Expose the ports for PostgreSQL, FastAPI, and Streamlit
EXPOSE 5432 8080 8501

# Start all services via the entrypoint script
CMD ["/usr/local/bin/entrypoint.sh"]
