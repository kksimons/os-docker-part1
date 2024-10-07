import streamlit as st
import requests
from datetime import date
import time

# Custom CSS for button styling, lord help me I don't know how to make the text stay white after click on streamlit
st.markdown(
    """
    <style>
    /* Target all buttons */
    div.stButton > button {
        background-color: #4CAF50;
        color: white;
        font-size: 16px;
        padding: 10px;
        border: none;
        cursor: pointer;
        border-radius: 4px;
        text-align: center;
    }

    div.stButton > button:hover {
        background-color: #45a049;
        color: white;
    }

    div.stButton > button:focus {
        background-color: #45a049;
        color: white;
        outline: none;
    }

    div.stButton > button:active {
        background-color: #45a049;
        color: white;
        outline: none;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# FastAPI URL
API_URL = "http://web:8080/student"

st.title("Student Record API Tester for OS")

# Input fields for student data creation
student_id = st.text_input("Student ID", value="12345")
student_name = st.text_input("Student Name", value="John Doe")
course = st.selectbox("Course", ["OS", "Math", "CS", "Physics"])
present_date = st.date_input("Present Date", value=date.today())


# POST request to create a student record
def create_student_record():
    # Add a delay to prevent Docker container issue
    time.sleep(5)  # Wait for 5 seconds just in case to prevent startup issues

    student_data = {
        "studentID": student_id,
        "studentName": student_name,
        "course": course,
        "presentDate": present_date.isoformat(),
    }

    # POST request for adding a student
    response = requests.post(API_URL, json=student_data)

    if response.status_code == 201:
        st.success("Student created successfully!")
        st.json(response.json())
    # 409 for conflict error
    elif response.status_code == 409:
        st.warning("Student already exists!")
        st.json(response.json())
    else:
        st.error(f"Error: {response.status_code}")
        st.text(response.text)


# GET request to retrieve all students
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


# GET request to retrieve a specific student by their ID
def get_student_by_id(student_id):
    response = requests.get(f"{API_URL}/{student_id}")

    if response.status_code == 200:
        student = response.json()
        st.success(f"Student with ID {student_id} found!")
        st.json(student)
    else:
        st.error(f"Error: {response.status_code}")
        st.text(response.text)


# Button to create a new student record
if st.button("Create Student Record"):
    create_student_record()

# Section for retrieving and displaying all students
st.subheader("Retrieve All Existing Records")
if st.button("Get All Students"):
    get_all_students()

# Section for retrieving a specific student by their ID
st.subheader("Retrieve a Single Student by ID")
specific_student_id = st.text_input("Enter Student ID to Retrieve")
if st.button("Get Student by ID"):
    get_student_by_id(specific_student_id)

st.write("Test to make sure we can't submit multiple of the same.")
