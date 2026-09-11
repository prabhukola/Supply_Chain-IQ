import numpy as np
from scipy.optimize import minimize

def optimize_order_quantities(df, total_budget=150000, max_capacity_units=10000):
    n = len(df)
    unit_costs = df["Unit_Cost"].values
    holding_costs = df["Unit_Cost"].values * 0.15
    order_costs = df["Order_Cost"].values
    demand = df["Monthly_Sales_Est"].values
    moqs = df["Moq"].values

    # Objective: Minimize Total Cost = Ordering Cost + Holding Cost
    def objective(Q):
        # Prevent zero division
        Q_safe = np.maximum(Q, 1e-5)
        total_order_cost = np.sum((demand / Q_safe) * order_costs)
        total_holding_cost = np.sum((Q_safe / 2.0) * holding_costs)
        return total_order_cost + total_holding_cost

    bounds = [(moqs[i], max(moqs[i] * 10, demand[i] * 3)) for i in range(n)]
    
    constraints = [
        {"type": "ineq", "fun": lambda Q: total_budget - np.sum(Q * unit_costs)}, # Budget
        {"type": "ineq", "fun": lambda Q: max_capacity_units - np.sum(Q)}         # Capacity
    ]

    initial_q = np.maximum(demand, moqs)

    res = minimize(objective, initial_q, method="SLSQP", bounds=bounds, constraints=constraints)

    baseline_q = np.maximum(demand, moqs)
    baseline_cost = float(objective(baseline_q))
    optimized_cost = float(res.fun) if res.success else baseline_cost

    optimized_q = res.x if res.success else baseline_q

    df_res = df.copy()
    df_res["Baseline_Order_Qty"] = np.round(baseline_q, 0)
    df_res["Optimized_Order_Qty"] = np.round(optimized_q, 0)
    df_res["Baseline_Cost"] = np.round((df_res["Baseline_Order_Qty"] * df_res["Unit_Cost"]), 2)
    df_res["Optimized_Cost"] = np.round((df_res["Optimized_Order_Qty"] * df_res["Unit_Cost"]), 2)

    return {
        "optimization_successful": res.success,
        "baseline_total_cost": round(baseline_cost, 2),
        "optimized_total_cost": round(optimized_cost, 2),
        "projected_savings": round(max(0, baseline_cost - optimized_cost), 2),
        "optimized_skus": df_res[["SKU_ID", "Baseline_Order_Qty", "Optimized_Order_Qty", "Baseline_Cost", "Optimized_Cost"]].head(15).to_dict(orient="records")
    }
