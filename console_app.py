from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27020")
db = client["university"]


def add_grade():
    student_id = input("Student ID: ")
    if not db.students.find_one({"student_id": student_id}):
        print("Student not found")
    course_code = input("Course code: ")
    grade = int(input("Grade: "))
    db.grades.update_one(
        {"student_id": student_id, "course_code": course_code},
        {
            "$set": {
                "grade": grade
            }
        },
        upsert=True
    )
    print("Grade saved")


def show_student_grades():
    student_id = input("Student ID: ")
    student = db.students.find_one({"student_id": student_id})  
    if not student:
        print("Student not found")
        return
    print(f"\n{student['first_name']} {student['last_name']}")
    pipeline = [
        {"$match": {"student_id": student_id}},
        {
            "$lookup": {
                "from": "courses",
                "localField": "course_code",
                "foreignField": "course_code",
                "as": "course"
            }
        },
        {"$unwind": "$course"}
    ]
    grades = db.grades.aggregate(pipeline)
    for g in grades:
        print(f"Course name - {g['course']['name']}, {g["type"]} job, Your grade - {g['grade']}")

def show_average():
    student_id = input("Student ID: ")
    result = list(db.grades.aggregate([
        {"$match": {"student_id": student_id}},
        {
            "$group": {
                "_id": "$student_id",
                "avg": {"$avg": "$grade"}
            }
        }
    ]))
    if result:
        print(f"Average: {round(result[0]['avg'], 2)}")
    else:
        print("No data")


def top_students():
    result = db.grades.aggregate([
        {
            "$group": {
                "_id": "$student_id",
                "avg": {"$avg": "$grade"}
            }
        },
        {"$sort": {"avg": -1}},
        {"$limit": 5}
    ])
    print("\nTop students:")
    for r in result:
        student = db.students.find_one({"student_id": r["_id"]})
        if student:
            print(f"{student['first_name']} {student['last_name']} → {round(r['avg'], 2)}")

def show_teacher_courses():
    teacher_id = input("Teacher ID: ")
    courses = db.courses.find({"teacher.id": teacher_id})
    found = False
    print("\nCourses:")
    for c in courses:
        print(f"{c['course_code']} - {c['name']} ({c['department']})")
        found = True
    if not found:
        print("No courses found")


while True:
    print("\n--- Teacher Console ---")
    print("1. Update grade")
    print("2. Show student grades")
    print("3. Show average")
    print("4. Top students")
    print("5. Teacher cources")
    print("6. Exit")

    choice = input("Choose: ")

    if choice == "1":
        add_grade()
    elif choice == "2":
        show_student_grades()
    elif choice == "3":
        show_average()
    elif choice == "4":
        top_students()
    elif choice == "5":
        show_teacher_courses()
    elif choice == "6":
        break
    else:
        print("Invalid choice")


