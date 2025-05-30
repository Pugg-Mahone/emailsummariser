from flask import Flask, request, jsonify, abort
import openai
import os

app = Flask(__name__)
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route("/", methods=["POST"])
def receive_email():
    try:
        # Raw dump of incoming request
        raw_data = request.get_data(as_text=True)
        app.logger.info(f"RAW BODY: {raw_data}")

        # Parsed JSON
        data = request.get_json(force=True, silent=True)
        app.logger.info(f"PARSED JSON: {data}")

        if not data:
            abort(400, description="Invalid or empty JSON")

        subject = data.get("subject", None)
        content = data.get("content", None)

        if not subject or not content:
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

    app.run(host="0.0.0.0", port=port)
