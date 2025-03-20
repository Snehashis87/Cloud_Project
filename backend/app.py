from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
import cv2
import numpy as np
from filters import apply_filter

app = Flask(__name__)
CORS(app)  # Enable CORS to prevent frontend issues

UPLOAD_FOLDER = "uploads"
PROCESSED_FOLDER = "processed"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

@app.route("/apply-filter", methods=["POST"])
def filter_image():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    filter_type = request.form.get("filter", "original")

    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    input_path = os.path.join(UPLOAD_FOLDER, file.filename)
    output_path = os.path.join(PROCESSED_FOLDER, file.filename)

    file.save(input_path)

    success = apply_filter(input_path, output_path, filter_type)
    
    if success:
        return send_file(output_path, mimetype="image/png")
    else:
        return jsonify({"error": "Failed to process image"}), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
