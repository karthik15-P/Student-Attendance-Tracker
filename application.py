from flask import Flask, render_template, request, redirect, url_for, flash
from database import get_db_connection, initialize_database
from datetime import date
import sqlite3

app = Flask(__name__)
app.secret_key = "student-attendance-secret-key"
initialize_database()

@app.route("/")
def index():
    conn = get_db_connection()
    total_students = conn.execute("SELECT COUNT(*) AS count FROM students").fetchone()["count"]
    total_classes = conn.execute("SELECT COUNT(DISTINCT date) AS count FROM attendance").fetchone()["count"]
    total_present = conn.execute("SELECT COUNT(*) AS count FROM attendance WHERE status = 'Present'").fetchone()["count"]
    total_records = conn.execute("SELECT COUNT(*) AS count FROM attendance").fetchone()["count"]
    overall_percentage = round(total_present / total_records * 100, 2) if total_records else 0
    conn.close()
    return render_template("index.html", total_students=total_students,
                           total_classes=total_classes,
                           overall_percentage=overall_percentage)

@app.route("/students")
def students():
    conn = get_db_connection()
    students = conn.execute("SELECT * FROM students ORDER BY roll_number").fetchall()
    conn.close()
    return render_template("students.html", students=students)

@app.route("/add_student", methods=["POST"])
def add_student():
    roll_number = request.form["roll_number"].strip()
    name = request.form["name"].strip()
    department = request.form["department"].strip()
    semester = request.form["semester"].strip()

    if not roll_number or not name:
        flash("Roll number and name are required.", "error")
        return redirect(url_for("students"))

    conn = get_db_connection()
    try:
        conn.execute("""
            INSERT INTO students (roll_number, name, department, semester)
            VALUES (?, ?, ?, ?)
        """, (roll_number, name, department, semester))
        conn.commit()
        flash("Student added successfully.", "success")
    except sqlite3.IntegrityError:
        flash("Roll number already exists.", "error")
    finally:
        conn.close()
    return redirect(url_for("students"))

@app.route("/delete_student/<int:student_id>", methods=["POST"])
def delete_student(student_id):
    conn = get_db_connection()
    conn.execute("DELETE FROM attendance WHERE student_id = ?", (student_id,))
    conn.execute("DELETE FROM students WHERE id = ?", (student_id,))
    conn.commit()
    conn.close()
    flash("Student deleted successfully.", "success")
    return redirect(url_for("students"))

@app.route("/attendance", methods=["GET", "POST"])
def attendance():
    conn = get_db_connection()
    students = conn.execute("SELECT * FROM students ORDER BY roll_number").fetchall()
    selected_date = request.args.get("date", date.today().isoformat())

    if request.method == "POST":
        selected_date = request.form["date"]
        for student in students:
            status = request.form.get(f"status_{student['id']}", "Absent")
            conn.execute("""
                INSERT INTO attendance (student_id, date, status)
                VALUES (?, ?, ?)
                ON CONFLICT(student_id, date)
                DO UPDATE SET status = excluded.status
            """, (student["id"], selected_date, status))
        conn.commit()
        conn.close()
        flash("Attendance recorded successfully.", "success")
        return redirect(url_for("attendance", date=selected_date))

    records = conn.execute(
        "SELECT student_id, status FROM attendance WHERE date = ?",
        (selected_date,)
    ).fetchall()
    existing_attendance = {r["student_id"]: r["status"] for r in records}
    conn.close()

    return render_template("attendance.html", students=students,
                           selected_date=selected_date,
                           existing_attendance=existing_attendance)

@app.route("/reports")
def reports():
    conn = get_db_connection()
    students = conn.execute("""
        SELECT s.id, s.roll_number, s.name, s.department, s.semester,
               COUNT(a.id) AS total_classes,
               SUM(CASE WHEN a.status = 'Present' THEN 1 ELSE 0 END) AS present_count
        FROM students s
        LEFT JOIN attendance a ON s.id = a.student_id
        GROUP BY s.id
        ORDER BY s.roll_number
    """).fetchall()

    student_reports = []
    for s in students:
        total = s["total_classes"]
        present = s["present_count"] or 0
        percentage = round(present / total * 100, 2) if total else 0
        student_reports.append({
            "roll_number": s["roll_number"],
            "name": s["name"],
            "department": s["department"],
            "semester": s["semester"],
            "total_classes": total,
            "present_count": present,
            "absent_count": total - present,
            "percentage": percentage
        })

    conn.close()
    return render_template("low_attendance.html", students=student_reports)

if __name__ == "__main__":
    app.run(debug=True)
