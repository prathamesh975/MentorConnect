from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)


mentors = [
    {
        "id": 1,
        "name": "Dr. Ananya Sharma",
        "expertise": "Machine Learning",
        "department": "Computer Science",
        "experience": 8,
        "slots": 3
    },
    {
        "id": 2,
        "name": "Prof. Rahul Mehta",
        "expertise": "Web Development",
        "department": "Computer Science",
        "experience": 6,
        "slots": 2
    },
    {
        "id": 3,
        "name": "Dr. Priya Nair",
        "expertise": "Data Science",
        "department": "Artificial Intelligence",
        "experience": 7,
        "slots": 4
    }
]


mentorship_requests = []


@app.route("/")
def home():
    return render_template("index.html", mentors=mentors)


@app.route("/mentors")
def mentor_list():
    return render_template("mentors.html", mentors=mentors)


@app.route("/request", methods=["GET", "POST"])
def mentorship_request():
    if request.method == "POST":
        student_name = request.form.get("student_name", "").strip()
        mentor_id = request.form.get("mentor_id", "").strip()
        topic = request.form.get("topic", "").strip()
        message = request.form.get("message", "").strip()

        if not student_name or not mentor_id or not topic or not message:
            return render_template(
                "requests.html",
                mentors=mentors,
                requests=mentorship_requests,
                error="All fields are required."
            )

        mentor = next(
            (mentor for mentor in mentors if str(mentor["id"]) == mentor_id),
            None
        )

        if mentor is None:
            return render_template(
                "requests.html",
                mentors=mentors,
                requests=mentorship_requests,
                error="Invalid mentor selected."
            )

        new_request = {
            "id": len(mentorship_requests) + 1,
            "student_name": student_name,
            "mentor": mentor["name"],
            "topic": topic,
            "message": message,
            "status": "Pending"
        }

        mentorship_requests.append(new_request)

        return redirect(url_for("requests_list"))

    return render_template(
        "requests.html",
        mentors=mentors,
        requests=mentorship_requests
    )


@app.route("/requests")
def requests_list():
    return render_template(
        "requests.html",
        mentors=mentors,
        requests=mentorship_requests
    )


@app.route("/requests/<int:request_id>/status", methods=["POST"])
def update_request_status(request_id):
    new_status = request.form.get("status", "").strip()

    allowed_statuses = ["Pending", "Accepted", "Completed"]

    if new_status not in allowed_statuses:
        return "Invalid status", 400

    mentorship_request = next(
        (
            item
            for item in mentorship_requests
            if item["id"] == request_id
        ),
        None
    )

    if mentorship_request is None:
        return "Request not found", 404

    mentorship_request["status"] = new_status

    return redirect(url_for("requests_list"))


@app.route("/api/mentors")
def api_mentors():
    return {
        "mentors": mentors
    }


@app.route("/api/requests")
def api_requests():
    return {
        "requests": mentorship_requests
    }


@app.route("/health")
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
