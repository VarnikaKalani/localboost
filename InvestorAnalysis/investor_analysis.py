import os
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Use Agg backend for non-GUI environments
import matplotlib.pyplot as plt

# ✅ Directory to save plots: InvestorAnalysis/static/plots
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_PLOTS_DIR = os.path.join(BASE_DIR, "..", "static", "plots")
os.makedirs(STATIC_PLOTS_DIR, exist_ok=True)

def save_plot(fig, filename):
    """Save plot to static/plots and return relative URL path."""
    path = os.path.join(STATIC_PLOTS_DIR, filename)
    fig.savefig(path, bbox_inches='tight', dpi=300)
    plt.close(fig)
    return f"/static/plots/{filename}"


def plot_monthly_growth(df):
    """✅ Plot monthly revenue growth matching the reference image."""
    df['Month'] = pd.to_datetime(df['Date']).dt.to_period('M').astype(str)
    monthly_sales = df.groupby('Month')['Revenue'].sum()

    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.bar(monthly_sales.index, monthly_sales.values, color='#87CEEB', edgecolor='black', width=0.6)

    ax.set_title("📈 Monthly Growth", fontsize=16, weight='bold', pad=15)
    ax.set_ylabel("Revenue", fontsize=13)
    ax.set_xlabel("Month", fontsize=13)
    ax.set_xticklabels(monthly_sales.index, rotation=45, fontsize=11)
    ax.set_yticklabels([f"{int(tick)}" for tick in ax.get_yticks()], fontsize=11)
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    ax.spines[['top', 'right']].set_visible(False)

    # Add data labels on top of bars
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f"{int(height)}",
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),  # Offset text
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=10, weight='bold')

    return save_plot(fig, "monthly_growth_plot.png")


def plot_product_distribution(df):
    """✅ Plot product revenue distribution matching the reference image."""
    product_sales = df.groupby('Product')['Revenue'].sum().sort_values()

    fig, ax = plt.subplots(figsize=(12, 12))
    bars = ax.barh(product_sales.index, product_sales.values, color='#6495ED', edgecolor='black')

    ax.set_title("🛍️ Product Revenue Distribution", fontsize=16, weight='bold', pad=15)
    ax.set_xlabel("Total Revenue", fontsize=13)
    ax.set_ylabel("Product", fontsize=13)
    ax.tick_params(axis='y', labelsize=10)
    ax.tick_params(axis='x', labelsize=11)
    ax.grid(axis='x', linestyle='--', alpha=0.7)
    ax.spines[['top', 'right']].set_visible(False)

    # Add revenue labels next to bars
    for bar in bars:
        width = bar.get_width()
        ax.annotate(f"${int(width)}",
                    xy=(width, bar.get_y() + bar.get_height() / 2),
                    xytext=(5, 0),
                    textcoords="offset points",
                    ha='left', va='center', fontsize=10, weight='bold')

    return save_plot(fig, "product_distribution_plot.png")


def plot_sales_performance(df):
    """✅ Plot weekly sales performance trend matching the reference image."""
    df['Date'] = pd.to_datetime(df['Date'])
    weekly_sales = df.resample('W-MON', on='Date')['Revenue'].sum().reset_index()

    fig, ax = plt.subplots(figsize=(12, 7))
    ax.plot(weekly_sales['Date'], weekly_sales['Revenue'],
            marker='o', linestyle='-', color='#2E8B57', linewidth=3, markersize=7, label='Weekly Sales')

    ax.set_title("📅 Weekly Sales Performance", fontsize=16, weight='bold', pad=10)
    ax.set_xlabel("Week Starting", fontsize=13)
    ax.set_ylabel("Total Revenue", fontsize=13)
    ax.tick_params(axis='x', rotation=45, labelsize=11)
    ax.tick_params(axis='y', labelsize=11)
    ax.grid(True, linestyle='--', alpha=0.7)
    ax.spines[['top', 'right']].set_visible(False)
    ax.legend(fontsize=12, loc='upper left')

    return save_plot(fig, "sales_performance_plot.png")


def run_investor_analysis(file_path):
    """✅ Run all plots and return their URLs."""
    df = pd.read_csv(file_path)
    df['Date'] = pd.to_datetime(df['Date'])

    return {
        "monthly_growth_plot": plot_monthly_growth(df),
        "product_distribution_plot": plot_product_distribution(df),
        "sales_performance_plot": plot_sales_performance(df)
    }
