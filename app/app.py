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

if st.button("Create Student Record"):
    create_student_record()

# Section for retrieving and displaying all students
st.subheader("Retrieve Existing Records")
if st.button("Get All Students"):
    get_all_students()

st.write("Test to make sure we can't submit multiple of the same.")

from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Date, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from datetime import date

# Database URL for PostgreSQL would move this into an .env in the future (localhost because all in one container now)
DATABASE_URL = "postgresql://user:password@localhost/StudentDB"

# Set up SQLAlchemy to interact with the database
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Student model representing the student table in the database
class Student(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True, index=True)
    studentid = Column(String, unique=True, index=True)  # Lowercase here
    studentname = Column(String)
    course = Column(String)
    presentdate = Column(Date, default=date.today)
    UniqueConstraint('studentid', name='uix_1')  # Ensure studentid is unique

# Create the tables in the database
Base.metadata.create_all(bind=engine)

# FastAPI app initialization
app = FastAPI()

# Pydantic model for handling POST request input
class StudentCreate(BaseModel):
    studentID: str
    studentName: str
    course: str
    presentDate: date = date.today()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# POST endpoint to create a student record
@app.post("/student", status_code=201)
def create_student(student: StudentCreate, db: SessionLocal = Depends(get_db)):
    # Check if student already exists by studentid
    existing_student = db.query(Student).filter(Student.studentid == student.studentID).first()  # Lowercase 'studentid'
    if existing_student:
        raise HTTPException(status_code=409, detail="Student already exists")
    
    # Create new student record
    new_student = Student(
        studentid=student.studentID,  # Lowercase 'studentid'
        studentname=student.studentName,  # Lowercase 'studentname'
        course=student.course,
        presentdate=student.presentDate  # Lowercase 'presentdate'
    )
    try:
        db.add(new_student)
        db.commit()
        db.refresh(new_student)
    except IntegrityError:
        raise HTTPException(status_code=409, detail="Student already exists")
    
    return {"message": "Student created successfully", "student": new_student}

# GET endpoint to retrieve a specific student by student_id
@app.get("/student/{student_id}")
def read_student(student_id: str, db: SessionLocal = Depends(get_db)):
    student = db.query(Student).filter(Student.studentid == student_id).first()  # Lowercase 'studentid'
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student
\
# add the get point for the streamlit
@app.get("/student")
def get_all_students(db: SessionLocal = Depends(get_db)):
    students = db.query(Student).all()
    if not students:
        raise HTTPException(status_code=404, detail="No students found")
    return students

# Part 2: PUT endpoint to update a student record. 
@app.put("/student/{student_id}", status_code=200)
def update_student(student_id: str, student: StudentCreate, db: SessionLocal = Depends(get_db)):
    # Check if student exists
    existing_student = db.query(Student).filter(Student.studentid == student_id).first()
    if not existing_student:
        raise HTTPException(status_code=404, detail="No student found with that ID")
    
    # Update the student record
    existing_student.studentname = student.studentName
    existing_student.course = student.course
    existing_student.presentdate = student.presentDate
    
    db.commit()
    db.refresh(existing_student)
    
    return {"message": "Student record updated successfully", "student": existing_student}

# Part 3: DELETE endpoint to delete a student record by student_id
@app.delete("/student/{student_id}", status_code=200)
def delete_student(student_id: str, db: SessionLocal = Depends(get_db)):
    # Check if student exists
    student = db.query(Student).filter(Student.studentid == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    # Delete the student record
    db.delete(student)
    db.commit()
    
    return {"message": "Student deleted successfully"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app="app:app", host="0.0.0.0", port=8080, reload=True)