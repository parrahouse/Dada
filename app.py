from flask import Flask, render_template, request, jsonify
import re

app = Flask(__name__)

def is_complete_sentence(text):
    return bool(re.match(r'^[A-Z].*[.?!]$', text))

def is_too_short(text):
    return len(text.split()) < 4

def prompt_for_detail(last_response):
    words = last_response.strip().split()
    if words:
        return f"What about {words[-1]}?"
    return "Can you say more?"

@app.route("/")
def home():
    return render_template("index.html", question="What is a strawberry?")

@app.route("/check", methods=["POST"])
def check_answer():
    answer = request.json["answer"]
    if not is_complete_sentence(answer):
        return jsonify({"feedback": "Can you say that in a full sentence?"})
    elif is_too_short(answer):
        return jsonify({"feedback": prompt_for_detail(answer)})
    else:
        return jsonify({"feedback": "That’s a complete answer! Good job."})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
