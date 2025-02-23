import os
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # To prevent GUI backend issues with Flask
import matplotlib.pyplot as plt

# ✅ Directory to save plots: static/plots
STATIC_PLOTS_DIR = os.path.join("static", "plots")
os.makedirs(STATIC_PLOTS_DIR, exist_ok=True)


def save_plot(fig, filename):
    plots_dir = os.path.join('static', 'plots')
    os.makedirs(plots_dir, exist_ok=True)  # ✅ Saves images to static/plots
    path = os.path.join(plots_dir, filename)
    fig.savefig(path, bbox_inches='tight')
    plt.close(fig)
    return f"static/plots/{filename}"


def plot_forecast(df):
    # Convert 'Date' column to datetime (if not already)
    df['Date'] = pd.to_datetime(df['Date'])

    # Aggregate revenue by week
    df_weekly = df.resample('W-MON', on='Date').sum().reset_index().sort_values('Date')

    fig, ax = plt.subplots(figsize=(12, 7))

    # Plot weekly sales trend
    ax.plot(df_weekly['Date'], df_weekly['Revenue'], marker='o', linestyle='-', color='dodgerblue',
            linewidth=3, label='Weekly Sales')

    # Plot styling
    ax.set_title("Weekly Sales Trend", fontsize=18, weight='bold', pad=15)
    ax.set_xlabel("Week Starting", fontsize=14)
    ax.set_ylabel("Total Revenue", fontsize=14)
    ax.legend(fontsize=12)
    ax.grid(True, linestyle='--', alpha=0.7)
    ax.tick_params(axis='x', rotation=45)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    return save_plot(fig, "forecast_plot.png")


def plot_revenue_trend(df):
    # Convert 'Date' column to datetime (if not already)
    df['Date'] = pd.to_datetime(df['Date'])

    # Aggregate revenue by week for a clearer trend
    df_weekly = df.resample('W-MON', on='Date').sum().reset_index().sort_values('Date')

    fig, ax = plt.subplots(figsize=(12, 7))

    # Plot weekly revenue trend
    ax.plot(df_weekly['Date'], df_weekly['Revenue'], marker='o', linestyle='-', color='seagreen',
            linewidth=3, label='Weekly Revenue')

    # Plot aesthetics
    ax.set_title("Weekly Revenue Trend", fontsize=18, weight='bold', pad=15)
    ax.set_xlabel("Week Starting", fontsize=14)
    ax.set_ylabel("Total Revenue", fontsize=14)
    ax.legend(fontsize=12)
    ax.grid(True, linestyle='--', alpha=0.7)
    ax.tick_params(axis='x', rotation=45)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    return save_plot(fig, "revenue_time_plot.png")



def plot_top_products(df):
    product_sales = df.groupby('Product')['Revenue'].sum().sort_values(ascending=False).head(5)
    fig, ax = plt.subplots(figsize=(8, 6))
    product_sales.plot(kind='bar', color='orange', ax=ax)
    ax.set_title("Top 5 Products", fontsize=14)
    ax.set_ylabel("Revenue", fontsize=12)
    ax.set_xlabel("Product", fontsize=12)
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    return save_plot(fig, "top_products_plot.png")


def sales_analysis(csv_file):
    """Main function to process CSV and generate plots."""
    df = pd.read_csv(csv_file)
    df['Date'] = pd.to_datetime(df['Date'])
    df.dropna(inplace=True)

    forecast_plot = plot_forecast(df)
    revenue_time_plot = plot_revenue_trend(df)
    top_products_plot = plot_top_products(df)

    return {
        "forecast_plot": forecast_plot,
        "revenue_time_plot": revenue_time_plot,
        "top_products_plot": top_products_plot
    }
