# LocalBoost 🚀

LocalBoost is a **hackathon project** designed to **empower small businesses** by providing a **data-driven toolkit** to:
- 📊 **Identify** top-selling products and services.
- 📈 **Track** daily sales performance.
- 🔮 **Forecast** future sales using ARIMA/SARIMA-based models.
- 🎯 **Make informed** business decisions backed by data insights.

---

## 📌 Features

✅ **Top Product Analysis** - Find out which products generate the most revenue.  
✅ **Sales Performance Dashboard** - Visualize daily sales trends with interactive charts.  
✅ **Sales Forecasting** - Automatically selects **ARIMA** or **SARIMA** models based on seasonality.  
✅ **Auto-Saved Reports** - All plots and insights are stored in the `static/plots` folder.  

---

## 📁 Project Structure

```
localboost/
├── data/                     # Contains sample CSV files
│   ├── sales_data_dummy.csv   # Example dataset
│   ├── sales_upload_template.csv
│   └── ...
├── env/                      # Virtual environment (optional)
├── Forecasting/              # Core sales forecasting scripts
│   ├── model.py              # Main analysis & forecasting script
│   ├── static/plots/         # Auto-saved charts & graphs
│   └── __pycache__/
├── InvestorAnalysis/         # Additional financial analytics
├── static/                   # Static files (for dashboards, etc.)
│   ├── plots/                # Directory where images are stored
├── templates/                # Web-based dashboard HTML templates
├── app.py                    # (Future) Web interface for visualization
├── README.md                 # Documentation (you are here)
└── requirements.txt          # Python dependencies
```

---

## ⚡ Getting Started

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/VarnikaKalani/localboost.git
cd localboost
```

### 2️⃣ Set Up a Virtual Environment (Recommended)
```bash
# Using conda:
conda create -n localboost_env python=3.9
conda activate localboost_env

# OR using venv:
python3 -m venv localboost_env
source localboost_env/bin/activate  # (Use `localboost_env\Scripts\activate` on Windows)
```

### 3️⃣ Install Required Dependencies
```bash
pip install -r requirements.txt
```

---

## 🚀 Usage

### 📌 Running the Analysis
1. **Prepare your dataset:**  
   - Your CSV file should contain at least:  
     **`Date`**, **`Product`**, **`Revenue`** columns.
   - Place it inside the `data/` folder (or update the script path accordingly).

2. **Run the main script:**
   ```bash
   cd Forecasting
   python model.py
   ```

3. **Results:**
   - The script analyzes **top products**, **sales trends**, and **forecasts future sales**.
   - **Generated charts** will be saved automatically in:
     ```
     Forecasting/static/plots/
     ```
   - Key plots include:
     - `top_products.png` (Most Profitable Products)
     - `sales_performance.png` (Daily Sales Trends)
     - `sales_forecast.png` (Future Sales Forecast)

---

## 📊 Roadmap
✔ **Optimize Forecast Models**: Improve ARIMA/SARIMA tuning for better accuracy.  
✔ **Interactive Web Dashboard**: Implement a Streamlit/Flask-based front-end.  
✔ **Extended Analytics**: Add cost data, profit margin insights, and regional performance tracking.  

---


## 📝 License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for more details.

---

🚀 **Built for small businesses. Empowered by data.** 🚀
