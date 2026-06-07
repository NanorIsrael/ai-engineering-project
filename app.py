import os
from flask import Flask, render_template, request, jsonify, session
import uuid

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "change-me-in-production")


SYSTEM_PROMPT = "You are a helpful assistant. Keep responses concise and conversational."


@app.route("/")
def index():
    if "session_id" not in session:
        session["session_id"] = str(uuid.uuid4())
        session["history"] = []
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "").strip()

    if not user_message:
        return jsonify({"error": "Empty message"}), 400

    if "history" not in session:
        session["history"] = []

    history = session["history"]
    history.append({"role": "user", "content": user_message})

    try:
        response = {
            "content":[{
                "text": "Hi human"
            }]
        }
        reply = response.get("content")[0].get("text")
        history.append({"role": "assistant", "content": reply})
        session["history"] = history
        session.modified = True
        return jsonify({"reply": reply})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/clear", methods=["POST"])
def clear():
    session["history"] = []
    session.modified = True
    return jsonify({"ok": True})


if __name__ == "__main__":
    app.run(debug=True, port='4000')
