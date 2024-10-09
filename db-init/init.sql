-- Create the students table if it doesn't exist
CREATE TABLE IF NOT EXISTS students (
    id SERIAL PRIMARY KEY,
    studentid VARCHAR(255) UNIQUE,
    studentname VARCHAR(255),
    course VARCHAR(255),
    presentdate DATE DEFAULT CURRENT_DATE
);
