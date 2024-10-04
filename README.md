# This is for Part 1 of the Docker Assignment at SAIT for OS

This project consists of a frontend with Streamlit to interact with the backend, which is a PostgreSQL database, both running in Docker containers.

# This project was based on the FastAPI and python script I built for my capstone here: https://github.com/kksimons/python-scheduler

## Prerequisites

Before you start, make sure you have Docker installed on your machine. You can follow instructions to install Docker from [here](https://docs.docker.com/get-docker/).

## Pull Docker Images

To get started, you can pull the pre-built Docker images for the backend (FastAPI) and frontend (Streamlit) from Docker Hub:

1. **Pull the FastAPI Backend Image:**
    ```bash
    docker pull kksimons/os-docker-part1-web:latest
    ```

2. **Pull the Streamlit Frontend Image:**
    ```bash
    docker pull kksimons/os-docker-part1-streamlit:latest
    ```

## Running the Containers

### Step 1: Run the Backend (FastAPI)

1. To run the backend, use this command:
    ```bash
    docker run -d kksimons/os-docker-part1-web:latest
    ```
   - `-d` runs the container in detached mode so you can keep it running in the background.
   
2. The FastAPI app should now be running and accessible at `http://localhost:8080` via Postman.

### Step 2: Run the Frontend (Streamlit)

1. After the backend is running, start the Streamlit frontend using this command:
    ```bash
    docker run kksimons/os-docker-part1-streamlit:latest
    ```
   - This command runs the Streamlit app in the foreground, so you'll see logs and outputs, including POST/GET request logs.
   
2. The Streamlit app should now be accessible at `http://localhost:8501`. You must be running the backend first in order to interaact with it properly.

### Step 3: Accessing the Applications

- **Backend (FastAPI)**: 
   - If you want to interact with the backend directly, you can use tools like **Postman** or **curl**. 
   - Example using `curl` to create a new student:
     ```bash
     curl -X POST "http://localhost:8080/student" -H "Content-Type: application/json" -d '{
         "studentID": "12345",
         "studentName": "John Doe",
         "course": "OS",
         "presentDate": "2024-10-03"
     }'
     ```
   - You can also use `http://localhost:8080` to interact with the FastAPI backend directly from the browser (for example, to view API documentation or access endpoints).

- **Frontend (Streamlit)**: Open your browser and navigate to `http://localhost:8501` to use the Streamlit app, which provides a user interface to interact with the backend.

### Step 4: Stopping Containers

If you want to stop both the backend and frontend containers after you've finished working, you can stop all running containers using this single command:

```bash
docker stop $(docker ps -q)
