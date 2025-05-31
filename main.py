from flask import Flask, request, jsonify
import os
import logging

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

@app.route("/", methods=["POST"])
def receive_email():
    raw_data = request.get_data(as_text=True)
    headers = dict(request.headers)
    app.logger.info(f"RAW BODY: {raw_data}")
    app.logger.info(f"HEADERS: {headers}")

    return jsonify({
        "raw": raw_data,
        "headers": headers
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
