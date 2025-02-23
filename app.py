from flask import Flask, render_template, request, redirect, url_for
import os
import pandas as pd
from Forecasting.model import sales_analysis
from InvestorAnalysis.investor_analysis import run_investor_analysis

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join('data', 'uploads')
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        uploaded_file = request.files.get("file")
        if uploaded_file and uploaded_file.filename.endswith(".csv"):
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
            uploaded_file.save(file_path)
            return redirect(url_for("results", filename=uploaded_file.filename))
        return render_template("index.html", error="Please upload a valid CSV file.")
    return render_template("index.html")


@app.route("/results/<filename>")
def results(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if not os.path.exists(file_path):
        return "File not found", 404

    try:
        # Run forecasting analysis
        forecasting_results = sales_analysis(file_path, forecast_steps=30)

        # Run investor analysis
        investor_results = run_investor_analysis(file_path)

        # Pass both forecasting and investor results to the template
        return render_template(
            "results.html",
            filename=filename,

            # Forecasting plots
            forecast_plot=forecasting_results["forecast_plot"],
            revenue_time_plot=forecasting_results["revenue_time_plot"],
            top_products_plot=forecasting_results["top_products_plot"],

            # Investor scores & plots
            investor_scores=investor_results["scores"],
            sales_forecast_plot=investor_results["sales_forecast_plot"],
            monthly_growth_plot=investor_results["monthly_growth_plot"],
            product_distribution_plot=investor_results["product_distribution_plot"]
        )

    except Exception as e:
        return f"⚠️ Error processing file: {str(e)}", 500


if __name__ == "__main__":
    app.run(debug=True, port=5001)
