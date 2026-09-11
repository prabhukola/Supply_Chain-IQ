import pandas as pd
import numpy as np

def compute_abc_xyz_matrix(df):
    df = df.copy()
    df["Revenue"] = df["Monthly_Sales_Est"] * df["Unit_Cost"]
    df = df.sort_values(by="Revenue", ascending=False)
    
    df["Cum_Revenue"] = df["Revenue"].cumsum()
    df["Total_Revenue"] = df["Revenue"].sum()
    df["Cum_Pct"] = df["Cum_Revenue"] / df["Total_Revenue"]

    # ABC Categorization
    def get_abc(pct):
        if pct <= 0.70: return "A"
        elif pct <= 0.90: return "B"
        else: return "C"
        
    df["ABC"] = df["Cum_Pct"].apply(get_abc)

    # Simulated Volatility Coefficient for XYZ (CV)
    np.random.seed(42)
    df["CV"] = np.round(np.random.uniform(0.05, 0.85, len(df)), 2)

    def get_xyz(cv):
        if cv <= 0.25: return "X"
        elif cv <= 0.55: return "Y"
        else: return "Z"

    df["XYZ"] = df["CV"].apply(get_xyz)
    df["ABC_XYZ"] = df["ABC"] + df["XYZ"]

    strategies = {
        "AX": "Just-In-Time (Automated Reorder)",
        "AY": "Safety Stock + Frequent Review",
        "AZ": "Buffer Stock + Manual Oversight",
        "BX": "Standard EOQ",
        "BY": "Periodic Review",
        "BZ": "Demand-Driven Replenishment",
        "CX": "Bulk Order (Low Touch)",
        "CY": "Consignment Stock",
        "CZ": "On-Demand Only / Drop-ship"
    }

    df["Strategy"] = df["ABC_XYZ"].map(strategies)
    matrix_counts = df["ABC_XYZ"].value_counts().to_dict()

    return {
        "matrix_distribution": matrix_counts,
        "classified_skus": df[["SKU_ID", "ABC", "XYZ", "ABC_XYZ", "Strategy"]].to_dict(orient="records")
    }
