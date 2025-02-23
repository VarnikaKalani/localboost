import pandas as pd
from investor_analysis import run_investor_analysis

# Load sample data
df = pd.read_csv("data/data/sales_data_dummy.csv")
df['Date'] = pd.to_datetime(df['Date'])

# Run analysis
run_investor_analysis(df)

