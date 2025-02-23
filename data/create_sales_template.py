import os
import pandas as pd

# ✅ Updated columns
columns = ["Date", "Product", "Quantity_Sold", "Revenue"]
df_template = pd.DataFrame(columns=columns)

# Ensure the 'data' folder exists
data_folder = os.path.join(os.getcwd(), "data", "data")
os.makedirs(data_folder, exist_ok=True)

# Save the template in the 'data' folder
output_path = os.path.join(data_folder, "sales_upload_template.csv")
df_template.to_csv(output_path, index=False)

print(f"✅ Template created successfully at: {output_path}")

