# Part 1 of the Docker Assignment at SAIT for OS

This project consists of a frontend with Streamlit and a backend with FastAPI, connected to a PostgreSQL database, all running within a single Docker container.

This project is based on the FastAPI and Python script developed for my capstone, which you can find [here](https://github.com/kksimons/python-scheduler).

Microsoft Visual C++ 14.0 or greater is required if you're running it from the source code found here, not needed when running from the Docker. Get it with "Microsoft C++ Build Tools": which you can find [here](https://visualstudio.microsoft.com/visual-cpp-build-tools/).

## Prerequisites

Before you start, make sure you have Docker installed on your machine. You can follow instructions to install Docker from [here](https://docs.docker.com/get-docker/).

## Pull Docker Image

To get started, pull the pre-built Docker image that contains both the backend (FastAPI) and frontend (Streamlit):

1. **Pull the Combined Docker Image:**
    ```bash
    docker pull kksimons/os-docker-part1-combined:latest
    ```

## Running the Container

### Step 1: Run the Combined Container

1. Use the following command to run the combined container:
    ```bash
    docker run -p 5438:5432 -p 8082:8080 -p 8508:8501 kksimons/os-docker-part1-combined:latest
    ```
   - The above command maps the container's ports to the host machine, I use different ports because of multiple instances of other things, feel free to change mappings to match your needs
     - PostgreSQL is accessible on `localhost:5438`
     - FastAPI is accessible on `localhost:8082`
     - Streamlit is accessible on `localhost:8508`
     
2. The FastAPI app should be running and accessible at `http://localhost:8082` if you want to use postman, while the Streamlit app frontend interface can be found at `http://localhost:8508`.

### Step 2: Accessing the Applications

- **Backend (FastAPI)**:
   - You can interact with the backend directly using tools like **Postman** or **curl**.
   - Example using `curl` to create a new student:
     ```bash
     curl -X POST "http://localhost:8082/student" -H "Content-Type: application/json" -d '{
         "studentID": "12345",
         "studentName": "John Doe",
         "course": "OS",
         "presentDate": "2024-10-03"
     }'
     ```

- **Frontend (Streamlit)**: Open your browser and go to `http://localhost:8508` to use the Streamlit app, which provides a user interface to interact with the backend.
