import os
from flask import Flask, render_template, request, jsonify, session
import uuid
import policy_assistant

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "change-me-in-production")


@app.route("/")
def index():
    if "session_id" not in session:
        session["session_id"] = str(uuid.uuid4())
        session["history"] = []
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_question = data.get("message", "").strip()

    if not user_question:
        return jsonify({"error": "Empty message"}), 400

    if "history" not in session:
        session["history"] = []

    history = session["history"]
    history.append({"role": "user", "content": user_question})

    try:
        if os.environ.get("ENVIRONMENT", "test") == 'test':
            response = {
                "content":[{
                    "text": "Hi human"
                }]
            }
            reply = response.get("content")[0].get("text")

        else:
            # response = {
            #     "content":[{
            #         "text": "Hi human"
            #     }]
            # }
            # reply = response.get("content")[0].get("text")

            response = policy_assistant.answer_and_sources(user_question)
            reply =  response.get("answer")
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

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"ok": True})

@app.route("/history", methods=["GET"])
def history():
    return jsonify(session.get("history", []))

if __name__ == "__main__":
    app.run(debug=True, port='4000')
