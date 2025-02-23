from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from model import sales_analysis  # Ensure this function works and returns the correct dict

app = Flask(__name__, static_folder='static')
CORS(app)  # Enable CORS for React access

# ✅ Correct upload folder path (from your structure)
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'data', 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/api/sales_forecast", methods=["GET","POST"])
def sales_forecast_api():
    if request.method == "GET":
        return jsonify({"message": "Use POST to upload CSV files."}), 200
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files['file']

    # Validate file extension
    if not file or not file.filename.endswith('.csv'):
        return jsonify({"error": "Invalid file format. Please upload a CSV file."}), 400

    # Save uploaded file to the uploads folder
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)

    try:
        # Call your sales_analysis function from model.py
        results = sales_analysis(file_path)
        
        # ✅ Ensure results has these keys: forecast_plot, revenue_time_plot, top_products_plot
        return jsonify({
            "forecast_plot": results.get("forecast_plot"),
            "revenue_time_plot": results.get("revenue_time_plot"),
            "top_products_plot": results.get("top_products_plot")
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5050)
