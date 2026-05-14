# test_sheets.py
from data.sheets import load_table

# Test loading each table
sales_df = load_table("Sales_Orders")
hr_df = load_table("HR_Employees")
customer_df = load_table("Customer_Details")

print("Sales Orders shape:", sales_df.shape)
print("HR Employees shape:", hr_df.shape)
print("Customer Details shape:", customer_df.shape)

print("\nFirst Sales Order row:")
print(sales_df.iloc[0])