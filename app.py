from flask import Flask, render_template, request, redirect, url_for
'''render_template = show the web page
request = get the data from forms
redirect = move to another page
'''
from database_connection import collection


app = Flask(__name__)# creats the website
app.secret_key = "student_management_secret_key"

attendance_stack = []

#ROUTE PAGE
@app.route("/")
def role_select():
    return render_template("role_select.html")


# TEACHER LOGIN PAGE
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":  #it checks wheather the user submitted the form
        Id = request.form["userid"]
        password = request.form["password"]

        if Id == "navya@le1" and password == "123":
            return redirect(url_for("dashboard"))
        else:
            return render_template("login.html", error="Invalid Username or Password")

    return render_template("login.html") # it will stay in that page


#STUDENT LOGIN PAGE
@app.route("/student-login", methods=["GET","POST"])
def student_login():
    if request.method == "POST":
        roll = request.form["roll"].upper()
        name = request.form["name"].upper()

        student = collection.find_one({"ROLL NO": roll, "NAME": name})

        if student:
            return redirect(url_for("student_dashboard", roll=roll))
        else:
            return render_template("student_login.html", error="Student not found")

    return render_template("student_login.html")

# DASHBOARD PAGE
@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html") # shows the dashboard page

@app.route("/attendance", methods=["GET", "POST"])
def attendance_page():
    students = list(collection.find())

    if request.method == "POST":
        session_attendance = []

        for student in students:
            roll_no = student["ROLL NO"]
            status = request.form.get(roll_no)

            if status == "P":
                collection.update_one(
                    {"ROLL NO": roll_no},
                    {"$inc": {"PRESENT_COUNT": 1}}
                )
                session_attendance.append({"ROLL NO": roll_no, "STATUS": "P"})

            elif status == "A":
                collection.update_one(
                    {"ROLL NO": roll_no},
                    {"$inc": {"ABSENT_COUNT": 1}}
                )
                session_attendance.append({"ROLL NO": roll_no, "STATUS": "A"})

        attendance_stack.append(session_attendance)

        return render_template(
            "attendance.html",
            students=students,
            success=True
        )

    return render_template("attendance.html", students=students)


@app.route("/academics", methods=["GET", "POST"])
def academics_page():
    student = None
    error = None

    if request.method == "POST":
        roll_no = request.form["roll_no"].upper()
        name = request.form["name"].upper()

        student = collection.find_one({"ROLL NO": roll_no, "NAME": name})

        if not student:
            error = "Student not found. Please check Roll Number."

    return render_template(
        "academics.html",
        student=student,
        error=error
    )

@app.route("/mark-academics/<roll_no>", methods=["GET", "POST"])
def mark_academics_page(roll_no):
    student = collection.find_one({"ROLL NO": roll_no})

    if not student:
        return "Student not found"

    success = False
    total = percentage = grade = result = None

    if request.method == "POST":
        dbms = int(request.form["dbms"])
        dlco = int(request.form["dlco"])
        ps   = int(request.form["ps"])
        ml   = int(request.form["ml"])
        ot   = int(request.form["ot"])

        marks = [dbms, dlco, ps, ml, ot]

        total = sum(marks)
        percentage = (total / 500) * 100
        average = total / 5

        if average >= 90:
            grade = "A"
        elif average >= 75:
            grade = "B"
        elif average >= 50:
            grade = "C"
        elif average >= 35:
            grade = "D"
        else:
            grade = "Fail"

        result = "Pass"
        for m in marks:
            if m < 35:
                result = "Fail"
                break

        collection.update_one(
            {"ROLL NO": roll_no},
            {"$set": {
                "DBMS": dbms,
                "DLCO": dlco,
                "P&S": ps,
                "ML": ml,
                "OT": ot,
                "TOTAL MARKS": total,
                "PERCENTAGE": percentage,
                "GRADE": grade,
                "RESULT": result
            }}
        )

        success = True

    return render_template(
        "mark_academics.html",
        student=student,
        success=success,
        total=total,
        percentage=percentage,
        grade=grade,
        result=result
    )

@app.route("/student-report/<roll_no>")
def student_report_page(roll_no):
    student = collection.find_one({"ROLL NO": roll_no})

    if not student:
        return "Student not found"

    return render_template(
        "student_report.html",
        student=student
    )

@app.route("/add-student", methods=["GET", "POST"])
def add_student_page():
    success = None
    error = None

    if request.method == "POST":
        roll_no = request.form["roll_no"].upper()
        name = request.form["name"].upper()
        branch = request.form["branch"].upper()
        phone_no = request.form["phone"]

        # Check if student already exists
        if collection.find_one({"ROLL NO": roll_no}):
            error = "Student with this Roll Number already exists."
        else:
            student_data = {
                "ROLL NO": roll_no,
                "NAME": name,
                "BRANCH": branch,
                "PHONE NO": phone_no,
                "PRESENT_COUNT": 0,
                "ABSENT_COUNT": 0,
                "RESULT": "NULL"
            }

            collection.insert_one(student_data)
            success = "✔ Student added successfully!"

    return render_template(
        "add_student.html",
        success=success,
        error=error
    )

@app.route("/attendance-rollback", methods=["GET", "POST"])
def attendance_rollback_page():

    message = None
    error = None

    if request.method == "POST":

        if len(attendance_stack) == 0:
            error = "Attendance is not recorded yet."
        else:
            last_session = attendance_stack.pop()

            for record in last_session:
                roll_no = record["ROLL NO"]
                status = record["STATUS"]

                if status == "P":
                    collection.update_one(
                        {"ROLL NO": roll_no},
                        {"$inc": {"PRESENT_COUNT": -1}}
                    )
                elif status == "A":
                    collection.update_one(
                        {"ROLL NO": roll_no},
                        {"$inc": {"ABSENT_COUNT": -1}}
                    )

            message = "✔ Attendance session undone successfully!"

    return render_template(
        "attendance_rollback.html",
        message=message,
        error=error
    )

@app.route("/class-report")
def class_report_page():

    students = list(collection.find())

    return render_template(
        "class_report.html",
        students=students
    )

@app.route("/student/dashboard/<roll>")
def student_dashboard(roll):
    student = collection.find_one({"ROLL NO": roll})
    return render_template(
        "student_dashboard.html",
        student=student
    )


@app.route("/student/attendance/<roll>")
def student_attendance(roll):
    student = collection.find_one({"ROLL NO": roll})
    present = student.get("PRESENT_COUNT", 0)
    absent = student.get("ABSENT_COUNT", 0)
    total = present + absent
    percentage = round((present / total) * 100, 2) if total > 0 else 0

    return render_template(
        "student_attendance.html",
        student=student,
        percentage=percentage
    )


@app.route("/student/academics/<roll>")
def student_academics(roll):
    student = collection.find_one({"ROLL NO": roll})
    return render_template("student_academics.html", student=student)


@app.route("/student/info/<roll>")
def student_info(roll):
    student = collection.find_one({"ROLL NO": roll})
    return render_template("student_info.html", student=student)
from flask import redirect, url_for, session

@app.route('/logout')
def logout():
    session.clear()   # clears student/teacher login data
    return redirect(url_for('role_select'))

if __name__ == "__main__":
    app.run(debug=True)