import os
import pandas as pd
import numpy as np

def generate_synthetic_data(file_path="data/sample_supply_chain.csv"):
    np.random.seed(42)
    n_samples = 100

    skus = [f"SKU-{1000 + i}" for i in range(n_samples)]
    suppliers = [f"SUP-{np.random.randint(1, 10):03d}" for _ in range(n_samples)]
    unit_costs = np.round(np.random.uniform(10, 500, n_samples), 2)
    current_stock = np.random.randint(5, 500, n_samples)
    monthly_sales = np.random.randint(20, 600, n_samples)
    lead_times = np.random.randint(3, 45, n_samples)
    defect_rates = np.round(np.random.uniform(0.1, 5.0, n_samples), 2)
    shipping_costs = np.round(unit_costs * np.random.uniform(0.05, 0.25, n_samples), 2)
    order_costs = np.round(np.random.uniform(50, 300, n_samples), 2)
    supplier_capacity = monthly_sales + np.random.randint(20, 300, n_samples)
    moq = np.random.choice([10, 25, 50, 100], n_samples)

    df = pd.DataFrame({
        "SKU_ID": skus,
        "Unit_Cost": unit_costs,
        "Current_Stock": current_stock,
        "Monthly_Sales_Est": monthly_sales,
        "Supplier_ID": suppliers,
        "Supplier_Lead_Time_Days": lead_times,
        "Defect_Rate_Pct": defect_rates,
        "Shipping_Cost": shipping_costs,
        "Order_Cost": order_costs,
        "Supplier_Capacity": supplier_capacity,
        "Moq": moq
    })

    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    df.to_csv(file_path, index=False)
    return df

def load_and_preprocess_data(file_path="data/sample_supply_chain.csv"):
    if not os.path.exists(file_path):
        df = generate_synthetic_data(file_path)
    else:
        df = pd.read_csv(file_path)

    # Engineered Features
    df["Inventory_Turnover_Est"] = (df["Monthly_Sales_Est"] * 12) / np.maximum(df["Current_Stock"], 1)
    df["Stock_Cover_Days"] = np.round((df["Current_Stock"] / np.maximum(df["Monthly_Sales_Est"], 1)) * 30, 1)
    df["Stockout_Risk_Flag"] = (df["Stock_Cover_Days"] < df["Supplier_Lead_Time_Days"]).astype(int)
    df["Total_Unit_Land_Cost"] = df["Unit_Cost"] + df["Shipping_Cost"]
    df["Revenue_Exposure"] = df["Monthly_Sales_Est"] * df["Unit_Cost"]
    df["Demand_Pressure_Index"] = np.round((df["Monthly_Sales_Est"] / np.maximum(df["Current_Stock"], 1)) * (df["Supplier_Lead_Time_Days"] / 10), 2)

    return df
