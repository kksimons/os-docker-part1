import streamlit as st
import requests
from datetime import date
import time

# Custom CSS for button styling
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

    /* Ensure text remains white on hover */
    div.stButton > button:hover {
        background-color: #45a049;
        color: white;
    }

    /* Ensure text remains white on focus/click */
    div.stButton > button:focus {
        background-color: #45a049;
        color: white;
        outline: none;
    }

    /* Ensure text remains white after clicking (active state) */
    div.stButton > button:active {
        background-color: #45a049;
        color: white;
        outline: none;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# FastAPI URL, have to change to localhost after putting all in one container
API_URL = "http://localhost:8080/student"

# Now need to login for JWT token, only get all will be tested with it for now
def login_user(username, password):
    response = requests.post("http://localhost:8080/login", json={"username": username, "password": password})
    if response.status_code == 200:
        token_data = response.json()
        st.session_state["token"] = token_data["access_token"]
        st.success("Logged in successfully!")
    else:
        st.error(f"Error: {response.status_code} - {response.text}")

# Example login form
username = st.text_input("Username")
password = st.text_input("Password", type="password")
if st.button("Log in"):
    login_user(username, password)


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
    elif response.status_code == 409:
        st.warning("Student already exists!")
        st.json(response.json())
    else:
        st.error(f"Error: {response.status_code}")
        st.text(response.text)


# GET request to retrieve all students
def get_all_students():
    if "token" not in st.session_state:
        st.warning("You need to log in first!")
        return
    
    headers = {
        "Authorization": f"Bearer {st.session_state['token']}"
    }
    
    response = requests.get(API_URL, headers=headers)
    
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

# Put Endpoint for Part 2
st.subheader("Update Existing Student Record")

update_student_id = st.text_input("Enter Student ID to Update", key="update_id")
update_student_name = st.text_input(
    "Updated Student Name", value="John Doe", key="update_name"
)
update_course = st.selectbox(
    "Updated Course", ["OS", "Math", "CS", "Physics"], key="update_course"
)
update_present_date = st.date_input(
    "Updated Present Date", value=date.today(), key="update_date"
)


# PUT request to update a student record
def update_student_record():
    student_data = {
        "studentID": update_student_id,
        "studentName": update_student_name,
        "course": update_course,
        "presentDate": update_present_date.isoformat(),
    }

    # Send PUT request
    response = requests.put(f"{API_URL}/{update_student_id}", json=student_data)

    if response.status_code == 200:
        st.success("Student updated successfully!")
        st.json(response.json())
    elif response.status_code == 404:
        st.warning("No student with that ID found")
        st.json(response.json())
    else:
        st.error(f"Error: {response.status_code}")
        st.text(response.text)


if st.button("Update Student Record"):
    update_student_record()

# DELETE request to remove a student record by student_id
def delete_student_record(student_id):
    response = requests.delete(f"{API_URL}/{student_id}")
    
    if response.status_code == 200:
        st.success("Student deleted successfully!")
        st.json(response.json())
    elif response.status_code == 404:
        st.warning("No student with that ID found.")
        st.json(response.json())
    else:
        st.error(f"Error: {response.status_code}")
        st.text(response.text)

# Section for deleting a student record by their ID
st.subheader("Delete Student Record")
delete_student_id = st.text_input("Enter Student ID to Delete", key="delete_id")
if st.button("Delete Student Record"):
    delete_student_record(delete_student_id)

st.write("Test to make sure we can't submit multiple of the same.")
