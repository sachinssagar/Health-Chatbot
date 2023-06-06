from flask import Flask, render_template, request, jsonify
import openai, os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

openai.api_key = os.getenv("OPENAI_API_KEY")


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    message = data["message"]
    condition = data.get("condition", "")
    severity = data.get("severity", "")

    response = generate_response(message, condition, severity)
    return jsonify({"response": response})


def generate_response(message, condition, severity):
    prompt = f"Condition: {condition}\nSeverity: {severity}\nUser: {message}\nChatGPT:"

    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=50,
        temperature=0.7,
        n=1,
        stop=None,
        timeout=10,
    )

    return response.choices[0].text.strip().replace("ChatGPT:", "")


if __name__ == "__main__":
    app.run(debug=True)
