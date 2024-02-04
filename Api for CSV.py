from fastapi import FastAPI, File, UploadFile, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
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

Base.metadata.create_all(bind=engine)

# Pydantic models for request payload
class StudentPayload(BaseModel):
    name: str
    age: int

class SubjectPayload(BaseModel):
    subject_id: int

class EnrollmentPayload(BaseModel):
    student: StudentPayload
    subjects: List[SubjectPayload]

# Function to insert data into SQL tables from CSV
def insert_data_from_csv(file: UploadFile):
    try:
        # Create a new session
        Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        db = Session()

        # Your CSV parsing and database insertion logic here
        import pandas as pd
        df = pd.read_csv(file.file)

        for _, row in df.iterrows():
            # Insert data into respective tables
            new_student = Student(name=row['student_name'], age=row['age'])
            db.add(new_student)
            db.flush()

            new_subject = Subject(subject_id=row['subject_id'])
            db.add(new_subject)
            db.flush()

            # Create the relationship in the enrollment table
            db.execute(enrollment_table.insert().values(student_id=new_student.id, subject_id=new_subject.id))

        # Commit the transaction
        db.commit()

        return {"message": "Data inserted successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# API endpoint for inserting data from CSV
@app.post("/insert-data-csv")
async def insert_data_csv_endpoint(file: UploadFile = File(...)):
    return insert_data_from_csv(file)