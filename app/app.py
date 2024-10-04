from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Date, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from datetime import date

# Database URL for PostgreSQL
DATABASE_URL = "postgresql://user:password@db/studentdb"

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

# add the get point for the streamlit
@app.get("/student")
def get_all_students(db: SessionLocal = Depends(get_db)):
    students = db.query(Student).all()
    if not students:
        raise HTTPException(status_code=404, detail="No students found")
    return students

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app="app:app", host="0.0.0.0", port=8080, reload=True)
