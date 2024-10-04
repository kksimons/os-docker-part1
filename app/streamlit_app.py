import streamlit as st
import requests
from datetime import date
import time

# FastAPI URL
API_URL = "http://web:8080/student"

# Title for the app
st.title("Student Record API Tester for OS")

# Input fields for student data
student_id = st.text_input("Student ID", value="12345")
student_name = st.text_input("Student Name", value="John Doe")
course = st.selectbox("Course", ["OS", "Math", "CS", "Physics"])
present_date = st.date_input("Present Date", value=date.today())

# Function to create a student record via POST request
def create_student_record():
    # Add a delay to prevent Docker container issue
    time.sleep(5)  # Wait for 5 seconds
    
    student_data = {
        "studentID": student_id,
        "studentName": student_name,
        "course": course,
        "presentDate": present_date.isoformat()
    }
    
    # Send POST request
    response = requests.post(API_URL, json=student_data)
    
    if response.status_code == 201:
        st.success("Student created successfully!")
        st.json(response.json())
    elif response.status_code == 409:
        st.warning("Student already exists!")
        st.json(response.json())
    else:
        st.error(f"Error: {response.status_code}")
        st.text(response.text)

# Function to retrieve all students via GET request
def get_all_students():
    time.sleep(5)  # Optional delay to ensure the server is ready
    
    # Send GET request to retrieve all students
    response = requests.get(API_URL)
    
    if response.status_code == 200:
        students = response.json()
        if len(students) > 0:
            st.success("Fetched students successfully!")
            st.json(students)  # Display list of students
        else:
            st.warning("No students found.")
    else:
        st.error(f"Error: {response.status_code}")
        st.text(response.text)

# Button to create a new student record
if st.button("Create Student Record"):
    create_student_record()

# Section for retrieving and displaying all students
st.subheader("Retrieve Existing Records")
if st.button("Get All Students"):
    get_all_students()

# Explanation for testing existing records
st.subheader("Testing Existing Records")
st.write("To test the handling of existing records, submit the same student data twice and observe the response.")
