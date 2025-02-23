import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Prevent GUI backend issues
import matplotlib.pyplot as plt
import os

# Create the 'plots' directory if it doesn't exist
plots_dir = 'static/plots'  # Ensure Flask serves from 'static' folder
os.makedirs(plots_dir, exist_ok=True)

def run_investor_analysis(file):
    """
    Run investor analysis on the uploaded CSV file and generate plots.

    Args:
        file: A file-like object (uploaded CSV file).

    Returns:
        dict: Paths to the generated plot images.
    """
    # Read the uploaded CSV file
    try:
        df = pd.read_csv(file, parse_dates=['Date'])
    except Exception as e:
        raise ValueError(f"Error reading CSV file: {e}")

    # Check for required columns
    required_columns = ['Date', 'Product', 'Revenue']
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        raise ValueError(f"Missing required columns: {', '.join(missing_columns)}")

    # Ensure 'Revenue' column is numeric
    df['Revenue'] = pd.to_numeric(df['Revenue'], errors='coerce')
    if df['Revenue'].isnull().any():
        raise ValueError("Revenue column contains invalid numeric values. Please check the data.")

    # Create 'Month' and 'Week' columns
    df['Month'] = df['Date'].dt.to_period('M').astype(str)
    df['Week'] = df['Date'].dt.to_period('W').apply(lambda r: r.start_time)

    # ----------------------------
    # 1️⃣ Monthly Growth Plot
    # ----------------------------
    monthly_growth = df.groupby('Month')['Revenue'].sum().reset_index()

    plt.figure(figsize=(10, 6))
    bars = plt.bar(monthly_growth['Month'], monthly_growth['Revenue'],
                   color='skyblue', edgecolor='black')
    plt.title('📈 Monthly Growth', fontsize=14, fontweight='bold')
    plt.xlabel('Month', fontsize=12)
    plt.ylabel('Revenue', fontsize=12)
    plt.xticks(rotation=45)

    # Annotate bars
    for bar in bars:
        height = bar.get_height()
        plt.annotate(f'{int(height)}', xy=(bar.get_x() + bar.get_width() / 2, height),
                     xytext=(0, 3), textcoords="offset points", ha='center',
                     fontsize=9, fontweight='bold')

    monthly_growth_plot_path = os.path.join(plots_dir, 'monthly_growth_plot.png')
    plt.tight_layout()
    plt.savefig(monthly_growth_plot_path)
    plt.close()

    # ----------------------------
    # 2️⃣ Product Revenue Distribution Plot
    # ----------------------------
    product_distribution = (
        df.groupby('Product')['Revenue']
        .sum()
        .sort_values(ascending=False)
        .reset_index()
    )

    plt.figure(figsize=(12, 10))
    bars = plt.barh(product_distribution['Product'], product_distribution['Revenue'],
                    color='cornflowerblue', edgecolor='black')
    plt.title('📊 Product Revenue Distribution', fontsize=14, fontweight='bold')
    plt.xlabel('Total Revenue', fontsize=12)
    plt.ylabel('Product', fontsize=12)

    # Annotate bars
    for bar in bars:
        width = bar.get_width()
        plt.annotate(f'${int(width)}', xy=(width, bar.get_y() + bar.get_height() / 2),
                     xytext=(5, 0), textcoords='offset points', va='center',
                     fontsize=9, fontweight='bold')

    product_distribution_plot_path = os.path.join(plots_dir, 'product_distribution_plot.png')
    plt.tight_layout()
    plt.savefig(product_distribution_plot_path)
    plt.close()

    # ----------------------------
    # 3️⃣ Weekly Sales Performance Plot
    # ----------------------------
    weekly_sales = df.groupby('Week')['Revenue'].sum().reset_index()

    plt.figure(figsize=(12, 6))
    plt.plot(weekly_sales['Week'], weekly_sales['Revenue'], marker='o',
             linestyle='-', color='seagreen', linewidth=2, label='Weekly Sales')
    plt.title('📅 Weekly Sales Performance', fontsize=14, fontweight='bold')
    plt.xlabel('Week Starting', fontsize=12)
    plt.ylabel('Total Revenue', fontsize=12)
    plt.xticks(rotation=45)
    plt.legend()

    sales_performance_plot_path = os.path.join(plots_dir, 'sales_performance_plot.png')
    plt.tight_layout()
    plt.savefig(sales_performance_plot_path)
    plt.close()

    # ----------------------------
    # ✅ Return the paths of the saved plots
    # ----------------------------
    return {
        "monthly_growth_plot": monthly_growth_plot_path.replace('static/', ''),
        "product_distribution_plot": product_distribution_plot_path.replace('static/', ''),
        "weekly_sales_performance_plot": sales_performance_plot_path.replace('static/', '')
    }
