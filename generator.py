import json
import random
from datetime import datetime, timedelta

NUM_STUDENTS = 1000
NUM_COURSES = 1000
NUM_GRADES = 1000

first_names = ["Ivan","Petr","Alex","Maria","Anna","Olga","Sergey","Dmitry","Nikita","Elena"]
last_names = ["Ivanov","Petrov","Sidorov","Smirnov","Kuznetsov","Popov","Sokolov","Lebedev"]

groups = ["CS-101","CS-102","CS-201","CS-202","SE-101","SE-201"]
faculties = ["Computer Science","Mathematics","Physics","Engineering"]

departments = ["CS","Math","Physics","AI","Software"]
teacher_names = [
    "Dr. Smith","Dr. Brown","Dr. Johnson",
    "Prof. Davis","Prof. Miller","Prof. Wilson"
]

types = ["exam","test","homework"]


def random_date():
    start = datetime(2023,1,1)
    end = datetime(2025,1,1)
    delta = end - start
    return (start + timedelta(days=random.randint(0, delta.days))).isoformat()


# ---------- STUDENTS ----------
students = []

for i in range(1, NUM_STUDENTS + 1):
    student_id = f"S2025{i:04d}"

    students.append({
        "student_id": student_id,
        "first_name": random.choice(first_names),
        "last_name": random.choice(last_names),
        "group": random.choice(groups),
        "faculty": random.choice(faculties),
        "year": random.randint(2022, 2025),
        "current_semester": random.randint(1, 8)
    })

with open("students.json","w") as f:
    for s in students:
        f.write(json.dumps(s) + "\n")


# ---------- COURSES ----------
courses = []

for i in range(1, NUM_COURSES + 1):

    courses.append({
        "course_code": f"C{i:04d}",
        "name": f"Course {i}",
        "teacher": {
            "id": f"T{random.randint(100,150)}",
            "name": random.choice(teacher_names)
        },
        "department": random.choice(departments),
        "credits": random.randint(2,5),
        "semester": random.randint(1,8)
    })

with open("courses.json","w") as f:
    for c in courses:
        f.write(json.dumps(c) + "\n")


# ---------- GRADES ----------
grades = []

for _ in range(NUM_GRADES):

    student = random.choice(students)
    course = random.choice(courses)

    grades.append({
        "student_id": student["student_id"],
        "course_code": course["course_code"],
        "semester": random.randint(1,8),
        "grade": random.randint(50,100),
        "date": random_date(),
        "type": random.choice(types)
    })

with open("grades.json","w") as f:
    for g in grades:
        f.write(json.dumps(g) + "\n")

print("Generated files:")
print("students.json")
print("courses.json")
print("grades.json")