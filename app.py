from flask import Flask, render_template, request, redirect, url_for
from database import create_tables, get_connection


app = Flask(__name__)


# Create database tables
create_tables()


# ==========================================
# DASHBOARD
# ==========================================

# ==========================================
# DASHBOARD
# ==========================================

@app.route("/")
def dashboard():

    connection = get_connection()

    # --------------------------------------
    # SUBJECT STATISTICS
    # --------------------------------------

    total_subjects = connection.execute("""
        SELECT COUNT(*) AS count
        FROM subjects
    """).fetchone()["count"]


    # --------------------------------------
    # TASK STATISTICS
    # --------------------------------------

    total_tasks = connection.execute("""
        SELECT COUNT(*) AS count
        FROM tasks
    """).fetchone()["count"]


    completed_tasks = connection.execute("""
        SELECT COUNT(*) AS count
        FROM tasks
        WHERE status = 'Completed'
    """).fetchone()["count"]


    pending_tasks = connection.execute("""
        SELECT COUNT(*) AS count
        FROM tasks
        WHERE status != 'Completed'
    """).fetchone()["count"]


    # --------------------------------------
    # STUDY HOURS
    # --------------------------------------

    study_hours = connection.execute("""
        SELECT COALESCE(SUM(duration), 0) AS total
        FROM study_sessions
    """).fetchone()["total"]


    # --------------------------------------
    # TASK COMPLETION PERCENTAGE
    # --------------------------------------

    if total_tasks > 0:

        completion_percentage = round(
            (completed_tasks / total_tasks) * 100
        )

    else:

        completion_percentage = 0


    # --------------------------------------
    # UPCOMING TASKS
    # --------------------------------------

    upcoming_tasks = connection.execute("""
        SELECT
            tasks.*,
            subjects.name AS subject_name

        FROM tasks

        JOIN subjects
        ON tasks.subject_id = subjects.id

        WHERE tasks.status != 'Completed'

        ORDER BY tasks.due_date ASC

        LIMIT 5
    """).fetchall()


    # --------------------------------------
    # UPCOMING EXAMS
    # --------------------------------------

    upcoming_exams = connection.execute("""
        SELECT *

        FROM subjects

        ORDER BY exam_date ASC

        LIMIT 5
    """).fetchall()


    connection.close()


    return render_template(
        "dashboard.html",

        total_subjects=total_subjects,

        total_tasks=total_tasks,

        completed_tasks=completed_tasks,

        pending_tasks=pending_tasks,

        study_hours=study_hours,

        completion_percentage=completion_percentage,

        upcoming_tasks=upcoming_tasks,

        upcoming_exams=upcoming_exams
    )


# ==========================================
# SUBJECTS
# ==========================================

@app.route("/subjects")
def subjects():
    connection = get_connection()

    subjects = connection.execute("""
        SELECT *
        FROM subjects
        ORDER BY exam_date ASC
    """).fetchall()

    connection.close()

    return render_template("subjects.html", subjects=subjects)


# ==========================================
# ADD SUBJECT
# ==========================================

@app.route("/subjects/add", methods=["GET", "POST"])
def add_subject():

    if request.method == "POST":

        name = request.form["name"]

        difficulty = request.form["difficulty"]

        exam_date = request.form["exam_date"]

        target_hours = request.form["target_hours"]


        connection = get_connection()

        connection.execute("""
            INSERT INTO subjects
            (name, difficulty, exam_date, target_hours)

            VALUES (?, ?, ?, ?)
        """, (
            name,
            difficulty,
            exam_date,
            target_hours
        ))


        connection.commit()

        connection.close()


        return redirect(url_for("subjects"))


    return render_template("add_subject.html")


# ==========================================
# EDIT SUBJECT
# ==========================================

@app.route(
    "/subjects/edit/<int:subject_id>",
    methods=["GET", "POST"]
)
def edit_subject(subject_id):

    connection = get_connection()


    if request.method == "POST":

        connection.execute("""
            UPDATE subjects

            SET name = ?,
                difficulty = ?,
                exam_date = ?,
                target_hours = ?

            WHERE id = ?
        """, (
            request.form["name"],
            request.form["difficulty"],
            request.form["exam_date"],
            request.form["target_hours"],
            subject_id
        ))


        connection.commit()

        connection.close()


        return redirect(url_for("subjects"))


    subject = connection.execute("""
        SELECT *
        FROM subjects

        WHERE id = ?
    """, (subject_id,)).fetchone()


    connection.close()


    return render_template(
        "edit_subject.html",
        subject=subject
    )


# ==========================================
# DELETE SUBJECT
# ==========================================

@app.route("/subjects/delete/<int:subject_id>")
def delete_subject(subject_id):

    connection = get_connection()


    # Delete related tasks
    connection.execute("""
        DELETE FROM tasks
        WHERE subject_id = ?
    """, (subject_id,))


    # Delete related study sessions
    connection.execute("""
        DELETE FROM study_sessions
        WHERE subject_id = ?
    """, (subject_id,))


    # Delete subject
    connection.execute("""
        DELETE FROM subjects
        WHERE id = ?
    """, (subject_id,))


    connection.commit()

    connection.close()


    return redirect(url_for("subjects"))


# ==========================================
# RUN APPLICATION
# ==========================================
# ==========================================
# TASKS
# ==========================================

@app.route("/tasks")
def tasks():

    connection = get_connection()

    tasks = connection.execute("""
        SELECT
            tasks.*,
            subjects.name AS subject_name
        FROM tasks
        JOIN subjects
        ON tasks.subject_id = subjects.id
        ORDER BY
            tasks.due_date ASC
    """).fetchall()

    connection.close()

    return render_template(
        "tasks.html",
        tasks=tasks
    )


# ==========================================
# ADD TASK
# ==========================================

@app.route("/tasks/add", methods=["GET", "POST"])
def add_task():

    connection = get_connection()

    subjects = connection.execute("""
        SELECT *
        FROM subjects
        ORDER BY name
    """).fetchall()


    if request.method == "POST":

        subject_id = request.form["subject_id"]

        title = request.form["title"]

        description = request.form["description"]

        due_date = request.form["due_date"]

        estimated_hours = request.form["estimated_hours"]


        connection.execute("""
            INSERT INTO tasks
            (
                subject_id,
                title,
                description,
                due_date,
                estimated_hours
            )

            VALUES (?, ?, ?, ?, ?)
        """, (
            subject_id,
            title,
            description,
            due_date,
            estimated_hours
        ))


        connection.commit()

        connection.close()


        return redirect(url_for("tasks"))


    connection.close()


    return render_template(
        "add_task.html",
        subjects=subjects
    )


# ==========================================
# COMPLETE TASK
# ==========================================

@app.route("/tasks/complete/<int:task_id>")
def complete_task(task_id):

    connection = get_connection()

    connection.execute("""
        UPDATE tasks

        SET status = 'Completed'

        WHERE id = ?
    """, (task_id,))


    connection.commit()

    connection.close()


    return redirect(url_for("tasks"))


# ==========================================
# DELETE TASK
# ==========================================

@app.route("/tasks/delete/<int:task_id>")
def delete_task(task_id):

    connection = get_connection()

    connection.execute("""
        DELETE FROM tasks

        WHERE id = ?
    """, (task_id,))


    connection.commit()

    connection.close()


    return redirect(url_for("tasks"))

# ==========================================
# STUDY TIMER
# ==========================================

@app.route("/timer")
def timer():

    connection = get_connection()

    subjects = connection.execute("""
        SELECT *
        FROM subjects
        ORDER BY name
    """).fetchall()

    connection.close()

    return render_template(
        "timer.html",
        subjects=subjects
    )


# ==========================================
# SAVE STUDY SESSION
# ==========================================

@app.route("/timer/save", methods=["POST"])
def save_session():

    from datetime import date

    subject_id = request.form["subject_id"]
    duration = float(request.form["duration"])

    if duration <= 0:
        return redirect(url_for("timer"))

    connection = get_connection()

    connection.execute("""
        INSERT INTO study_sessions
        (subject_id, duration, date)
        VALUES (?, ?, ?)
    """, (
        subject_id,
        duration,
        date.today().isoformat()
    ))

    connection.commit()
    connection.close()

    return redirect(url_for("timer"))

@app.route("/analytics")
def analytics():
    connection = get_connection()

    # Total study hours
    total_hours = connection.execute("""
        SELECT COALESCE(SUM(duration), 0) AS total
        FROM study_sessions
    """).fetchone()["total"]

    # Number of study sessions
    total_sessions = connection.execute("""
        SELECT COUNT(*) AS count
        FROM study_sessions
    """).fetchone()["count"]

    # Average session duration
    average_session = connection.execute("""
        SELECT COALESCE(AVG(duration), 0) AS average
        FROM study_sessions
    """).fetchone()["average"]

    # Study hours by subject
    subject_stats = connection.execute("""
        SELECT
            subjects.name AS subject_name,
            COALESCE(SUM(study_sessions.duration), 0) AS hours
        FROM study_sessions
        JOIN subjects
        ON study_sessions.subject_id = subjects.id
        GROUP BY study_sessions.subject_id
        ORDER BY hours DESC
    """).fetchall()

    # Study activity for the last 7 days
    weekly_stats = connection.execute("""
        SELECT
            date,
            COALESCE(SUM(duration), 0) AS hours
        FROM study_sessions
        WHERE date >= date('now', '-6 days')
        GROUP BY date
        ORDER BY date ASC
    """).fetchall()

    connection.close()

    return render_template(
        "analytics.html",
        total_hours=total_hours,
        total_sessions=total_sessions,
        average_session=average_session,
        subject_stats=subject_stats,
        weekly_stats=weekly_stats
    )

@app.route("/study-plan")
def study_plan():
    from datetime import date

    connection = get_connection()

    subjects = connection.execute("""
        SELECT *
        FROM subjects
        ORDER BY exam_date ASC
    """).fetchall()

    plans = []

    today = date.today()

    for subject in subjects:

        exam_date = date.fromisoformat(subject["exam_date"])
        days_left = (exam_date - today).days

        # Study hours already completed for this subject
        result = connection.execute("""
            SELECT COALESCE(SUM(duration), 0) AS studied
            FROM study_sessions
            WHERE subject_id = ?
        """, (subject["id"],)).fetchone()

        studied_hours = result["studied"]

        target_hours = float(subject["target_hours"])

        remaining_hours = max(target_hours - studied_hours, 0)

        if days_left > 0:
            daily_hours = remaining_hours / days_left
        else:
            daily_hours = remaining_hours

        if target_hours > 0:
            progress = min(
                round((studied_hours / target_hours) * 100),
                100
            )
        else:
            progress = 0

        plans.append({
            "name": subject["name"],
            "exam_date": subject["exam_date"],
            "days_left": days_left,
            "target_hours": target_hours,
            "studied_hours": studied_hours,
            "remaining_hours": remaining_hours,
            "daily_hours": daily_hours,
            "progress": progress,
            "difficulty": subject["difficulty"]
        })

    connection.close()

    return render_template(
        "study_plan.html",
        plans=plans
    )

@app.route("/pomodoro")
def pomodoro():
    connection = get_connection()

    subjects = connection.execute("""
        SELECT *
        FROM subjects
        ORDER BY name
    """).fetchall()

    connection.close()

    return render_template("pomodoro.html", subjects=subjects)


@app.route("/pomodoro/save", methods=["POST"])
def save_pomodoro():
    from datetime import date

    subject_id = request.form["subject_id"]
    duration = float(request.form["duration"])

    if duration <= 0:
        return redirect(url_for("pomodoro"))

    connection = get_connection()

    connection.execute("""
        INSERT INTO study_sessions
        (subject_id, duration, date)
        VALUES (?, ?, ?)
    """, (
        subject_id,
        duration,
        date.today().isoformat()
    ))

    connection.commit()
    connection.close()

    return redirect(url_for("pomodoro"))

@app.route("/sessions")
def sessions():

    connection = get_connection()

    sessions = connection.execute("""
        SELECT
            study_sessions.id,
            study_sessions.duration,
            study_sessions.date,
            subjects.name AS subject_name
        FROM study_sessions
        JOIN subjects
        ON study_sessions.subject_id = subjects.id
        ORDER BY study_sessions.id DESC
    """).fetchall()

    connection.close()

    total_hours = sum(session["duration"] for session in sessions)

    return render_template(
        "sessions.html",
        sessions=sessions,
        total_hours=total_hours
    )


@app.route("/sessions/delete/<int:session_id>")
def delete_session(session_id):

    connection = get_connection()

    connection.execute("""
        DELETE FROM study_sessions
        WHERE id = ?
    """, (session_id,))

    connection.commit()
    connection.close()

    return redirect(url_for("sessions"))

@app.route("/settings", methods=["GET", "POST"])
def settings():

    connection = get_connection()

    if request.method == "POST":

        name = request.form.get("name", "Student")
        study_mode = request.form.get(
            "study_mode",
            "Focused Learner"
        )

        daily_goal = request.form.get(
            "daily_goal",
            3
        )

        pomodoro_duration = request.form.get(
            "pomodoro_duration",
            25
        )

        connection.execute("""
            UPDATE settings
            SET
                name = ?,
                study_mode = ?,
                daily_goal = ?,
                pomodoro_duration = ?
            WHERE id = 1
        """, (
            name,
            study_mode,
            daily_goal,
            pomodoro_duration
        ))

        connection.commit()
        connection.close()

        return redirect(url_for("settings"))

    settings_data = connection.execute("""
        SELECT *
        FROM settings
        WHERE id = 1
    """).fetchone()

    connection.close()

    return render_template(
        "settings.html",
        settings=settings_data
    )

if __name__ == "__main__":
    app.run(debug=True)