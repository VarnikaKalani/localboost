import pandas as pd
import numpy as np

def generate_extended_sales_data(output_csv="sales_data_dummy_extended.csv",
                                 start_date="2022-01-01",
                                 end_date="2023-12-31"):
    """
    Generates daily sales data with:
    - Baseline revenue
    - Weekly seasonality (sinusoidal pattern)
    - Linear upward trend
    - Random noise

    Saves as a CSV with columns: Date, Revenue
    """

    # Create a daily date range
    dates = pd.date_range(start=start_date, end=end_date, freq='D')

    # Fix a random seed for reproducibility
    np.random.seed(42)

    data = []
    for i, d in enumerate(dates):
        # Baseline revenue
        baseline = 100

        # Weekly seasonality (day_of_week: Monday=0, Sunday=6)
        day_of_week = d.weekday()  # integer 0–6
        weekly_factor = 20 * np.sin(2 * np.pi * day_of_week / 7.0)

        # Upward trend over time
        trend = 0.2 * i  # tweak as needed

        # Random noise
        noise = np.random.normal(loc=0, scale=5)  # mean=0, std=5

        # Final revenue
        revenue = baseline + weekly_factor + trend + noise
        data.append([d.strftime("%Y-%m-%d"), round(revenue, 2)])

    # Convert to DataFrame and save to CSV
    df = pd.DataFrame(data, columns=["Date", "Revenue"])
    df.to_csv(output_csv, index=False)
    print(f"Generated {len(df)} rows of sales data in '{output_csv}'.")

if __name__ == "__main__":
    generate_extended_sales_data()
