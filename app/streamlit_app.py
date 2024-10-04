import streamlit as st
import requests
from datetime import date
import time

# FastAPI URL
API_URL = "http://web:8080/student"

st.title("Student Record API Tester for OS")

student_id = st.text_input("Student ID", value="12345")
student_name = st.text_input("Student Name", value="John Doe")
course = st.selectbox("Course", ["OS", "Math", "CS", "Physics"])
present_date = st.date_input("Present Date", value=date.today())

# POST request to simulate what's wanted in part 1 requirement doc
def create_student_record():
    # Add a delay to prevent Docker container issue
    time.sleep(5)  # Wait for 5 seconds just in case to prevent startup issues
    
    student_data = {
        "studentID": student_id,
        "studentName": student_name,
        "course": course,
        "presentDate": present_date.isoformat()
    }
    
    # POST request for adding a student
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

#let's add a get as well so we can see our handy-work
def get_all_students():
    
    response = requests.get(API_URL)
    
    if response.status_code == 200:
        students = response.json()
        if len(students) > 0:
            st.success("Fetched students successfully!")
            st.json(students)  
        else:
            st.warning("No students found.")
    else:
        st.error(f"Error: {response.status_code}")
        st.text(response.text)

# for interacting with the post
if st.button("Create Student Record"):
    create_student_record()

# let's add another one to get a specific student by their id
def get_student_by_id(student_id):
    response = requests.get(f"{API_URL}/{student_id}")
    
    if response.status_code == 200:
        student = response.json()
        st.success(f"Student with ID {student_id} found!")
        st.json(student)
    else:
        st.error(f"Error: {response.status_code}")
        st.text(response.text)

# for interacting with the get
st.subheader("Retrieve Existing Records")
if st.button("Get All Students"):
    get_all_students()

# for interacting with the post to get a specific student
st.subheader("Retrieve a Student by ID")
specific_student_id = st.text_input("Enter Student ID to Retrieve")
if st.button("Get Student by ID"):
    get_student_by_id(specific_student_id)

st.write("Test to make sure we can't submit multiple of the same.")
