from flask import Flask, request, jsonify
import openai
import os
import logging

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route("/", methods=["POST"])
def receive_email():
    try:
        raw_data = request.get_data(as_text=True)
        headers = dict(request.headers)
        app.logger.info(f"RAW BODY: {raw_data}")
        app.logger.info(f"HEADERS: {headers}")

        data = request.get_json(force=True, silent=True)
        subject = data.get("Subject", None)
        content = data.get("Content", None)

        if not subject or not content:
            return jsonify({"error": "Missing subject or content"}), 400

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
