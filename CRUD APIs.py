from fastapi import FastAPI, File, UploadFile, HTTPException, Depends
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel
from sqlalchemy.orm import sessionmaker, Session, relationship
from database import SessionLocal
from typing import List

app = FastAPI()

# Define the database connection for MySQL
DATABASE_URL = "mysql+pymysql://root@localhost:3306/test"
engine = create_engine(DATABASE_URL)
Base = declarative_base()

# Define the student table
class Student(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True)
    age = Column(Integer)

# Define the subject table
class Subject(Base):
    __tablename__ = "subjects"
    id = Column(Integer, primary_key=True, index=True)
    subject_id = Column(Integer)

# Define the enrollment table for Many-to-Many relationship
enrollment_table = Table(
    "enrollments",
    Base.metadata,
    Column("student_id", Integer, ForeignKey("students.id")),
    Column("subject_id", Integer, ForeignKey("subjects.id")),
)


# Pydantic models for request payload
class StudentPayload(BaseModel):
    name: str
    age: int

class SubjectPayload(BaseModel):
    subject_id: int

class EnrollmentPayload(BaseModel):
    student: StudentPayload
    subjects: List[SubjectPayload]

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Function to insert data into SQL tables from payload
def create_enrollment(payload: EnrollmentPayload, db: Session = Depends(get_db)):
    try:
        # Insert student data
        new_student = Student(name=payload.student.name, age=payload.student.age)
        db.add(new_student)
        db.flush()

        # Insert subjects data and handle Many-to-Many relationships
        for subject in payload.subjects:
            new_subject = Subject(subject_id=subject.subject_id)
            db.add(new_subject)
            db.flush()

            # Create the relationship in the enrollment table
            db.execute(enrollment_table.insert().values(student_id=new_student.id, subject_id=new_subject.id))

        # Commit the transaction
        db.commit()

        return {"message": "Data inserted successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# CRUD operation: Read - Get all students
@app.get("/students/", response_model=List[Student])
def get_students(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    students = db.query(Student).offset(skip).limit(limit).all()
    return students

# CRUD operation: Read - Get a specific student by ID
@app.get("/students/{student_id}", response_model=Student)
def get_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

# CRUD operation: Update - Update a specific student by ID
@app.put("/students/{student_id}", response_model=Student)
def update_student(student_id: int, payload: StudentPayload, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")

    student.name = payload.name
    student.age = payload.age
    db.commit()
    db.refresh(student)
    return student

# CRUD operation: Delete - Delete a specific student by ID
@app.delete("/students/{student_id}", response_model=dict)
def delete_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")

    db.delete(student)
    db.commit()

    return {"message": "Student deleted successfully"}