import openai
import os
from flask import Flask, request, jsonify, abort

app = Flask(__name__)

# Set up your OpenAI key
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route("/", methods=["POST"])
def receive_email():
    try:
        if not request.is_json:
            abort(400, description="Content-Type must be application/json")

        data = request.get_json(force=True, silent=True)
        app.logger.info(f"Received data: {data}")

        subject = data.get("subject", "")
        content = data.get("content", "")

        if not subject and not content:
            abort(400, description="Missing 'subject' and 'content' fields")

        prompt = f"Summarise the following email:\nSubject: {subject}\nContent: {content}"

        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )

        summary = response.choices[0].message.content.strip()
        return jsonify({"summary": summary})

    except Exception as e:
        app.logger.exception("Error processing request")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
