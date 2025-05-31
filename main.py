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
