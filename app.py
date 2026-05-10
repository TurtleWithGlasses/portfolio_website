from flask import Flask, render_template, request, jsonify, redirect
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)


@app.before_request
def enforce_https():
    if not app.debug and request.headers.get("X-Forwarded-Proto", "http") == "http":
        return redirect(request.url.replace("http://", "https://", 1), code=301)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/contact", methods=["POST"])
def contact():
    data = request.get_json(silent=True) or {}
    name = data.get("name", "").strip()
    email = data.get("email", "").strip()
    subject = data.get("subject", "").strip()
    message = data.get("message", "").strip()

    if not name or not email or not message:
        return jsonify({"status": "error", "message": "Name, email and message are required."}), 400

    # TODO: wire up email sending (e.g. smtplib or SendGrid)
    app.logger.info("Contact form — from: %s <%s> | subject: %s", name, email, subject)

    return jsonify({"status": "ok", "message": "Message received."})


if __name__ == "__main__":
    debug = os.getenv("FLASK_DEBUG", "true").lower() == "true"
    port = int(os.getenv("PORT", 5000))
    app.run(debug=debug, port=port)
