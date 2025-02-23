from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from investor_analysis import run_investor_analysis

app = Flask(__name__, static_folder='InvestorAnalysis/static')
CORS(app)

UPLOAD_FOLDER = os.path.join(os.getcwd(), 'InvestorAnalysis', 'data', 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/api/investor_analysis", methods=["POST"])
def investor_analysis_api():
    """Handle CSV upload and return plot URLs."""
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request."}), 400

    file = request.files['file']
    if not file.filename.endswith('.csv'):
        return jsonify({"error": "Invalid file format. Please upload a CSV."}), 400

    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)

    try:
        results = run_investor_analysis(file_path)
        return jsonify(results), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5054)
