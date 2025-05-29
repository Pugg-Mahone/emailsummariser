from flask import Flask, request, jsonify
import openai
app = Flask(__name__)
@app.route("/", methods=["POST"])
def receive_email():
    data = request.json
    subject = data.get("subject", "")
    content = data.get("content", "")

    prompt = f"Summarise the following email:\nSubject: {subject}\nContent: {content}"

    response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[{"role": "user", "content": prompt}]
    )

    summary = response.choices[0].message["content"].strip()
    return jsonify({"summary": summary})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=81)

