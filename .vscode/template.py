
#Creating Sales template
import os
import pandas as pd


# Creating Sales template
columns = ["Date", "Product/Service", "Sales_Amount", "Quantity_Sold", "Promotion"]
df_template = pd.DataFrame(columns=columns)

# Save CSV to the current working directory
output_path = os.path.join(os.getcwd(), "sales_upload_template.csv")
df_template.to_csv(output_path, index=False)

print(f"Template created successfully at: {output_path}")

