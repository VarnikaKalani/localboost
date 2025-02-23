from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
from investor_analysis import run_investor_analysis

app = Flask(__name__, static_folder='static')
CORS(app)

# Create upload and plots directories
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
PLOTS_FOLDER = os.path.join(app.static_folder, 'plots')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PLOTS_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/api/investor_analysis', methods=['POST'])
def investor_analysis():
    """Handle CSV upload, process data, and return plot URLs."""
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request."}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected."}), 400

    if not file.filename.endswith('.csv'):
        return jsonify({"error": "Invalid file format. Please upload a CSV."}), 400

    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)

    try:
        results = run_investor_analysis(file_path)
        plot_urls = {
            "monthly_growth_plot_url": f"/static/plots/{os.path.basename(results['monthly_growth_plot'])}",
            "product_distribution_plot_url": f"/static/plots/{os.path.basename(results['product_distribution_plot'])}",
            "weekly_sales_performance_plot_url": f"/static/plots/{os.path.basename(results['weekly_sales_performance_plot'])}"
        }
        return jsonify(plot_urls), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/static/plots/<filename>')
def serve_plot(filename):
    """Serve saved plot images."""
    return send_from_directory(PLOTS_FOLDER, filename)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5054, debug=True)


