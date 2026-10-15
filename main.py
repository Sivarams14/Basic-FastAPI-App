
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Initialize FastAPI application
app = FastAPI(
    title="My First FastAPI Application",
    description="CAIE Assignment 4 - Basic API Development",
    version="1.0.0"
)

# Sample data (stored in memory)
students = {
    1: {"name": "Sivaram", "course": "GenAI Course", "score": 99},
    2: {"name": "Krishna", "course": "Finance Course", "score": 99},
    3: {"name": "Shanmuga", "course": "Stock Market Course", "score": 99}
}

# Define structure for student data
class Student(BaseModel):
    name: str
    course: str
    score: int


# 1. ROOT ENDPOINT - GET
@app.get("/")
def home():
    return {
        "message": "Welcome to my first FastAPI application!",
        "status": "success",
        "developer": "Sivaram"
    }


# 2. GREETING ENDPOINT - GET with path parameter
@app.get("/greet/{name}")
def greet_user(name: str):
    return {
        "message": f"Hello {name}, welcome to FastAPI!"
    }


# 3. GREETING ENDPOINT - GET with query parameter
@app.get("/welcome")
def welcome_user(name: str, course: str = "FastAPI"):
    return {
        "message": f"Welcome {name}!",
        "course": course
    }


# 4. GET ALL STUDENTS
@app.get("/students")
def get_students():
    return {
        "total_students": len(students),
        "students": students
    }


# 5. GET STUDENT BY ID
@app.get("/students/{student_id}")
def get_student(student_id: int):

    if student_id not in students:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    return {
        "student_id": student_id,
        "student": students[student_id]
    }


# 6. CREATE STUDENT - POST

# CREATE STUDENT WITH A SPECIFIC ID
@app.post("/students/{student_id}", status_code=201)
def create_student_with_id(student_id: int, student: Student):

    # Check whether the student ID already exists
    if student_id in students:
        raise HTTPException(
            status_code=409,
            detail="Student ID already exists"
        )

    # Add student using the ID provided in the URL
    students[student_id] = student.model_dump()

    return {
        "message": "Student created successfully",
        "student_id": student_id,
        "student": students[student_id]
    }



# 7. UPDATE STUDENT - PUT
@app.put("/students/{student_id}")
def update_student(student_id: int, student: Student):

    if student_id not in students:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    students[student_id] = student.model_dump()

    return {
        "message": "Student updated successfully",
        "student": students[student_id]
    }


# 8. DELETE STUDENT - DELETE
@app.delete("/students/{student_id}")
def delete_student(student_id: int):

    if student_id not in students:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    deleted_student = students.pop(student_id)

    return {
        "message": "Student deleted successfully",
        "deleted_student": deleted_student
    }
