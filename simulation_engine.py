from app.services.health_engine import calculate_health_score

def run_crisis_simulation(df, demand_surge_pct=30.0, lead_time_delay_days=5, shipping_cost_increase_pct=15.0):
    sim_df = df.copy()

    # Apply Shocks
    sim_df["Monthly_Sales_Est"] = sim_df["Monthly_Sales_Est"] * (1 + demand_surge_pct / 100.0)
    sim_df["Supplier_Lead_Time_Days"] = sim_df["Supplier_Lead_Time_Days"] + lead_time_delay_days
    sim_df["Shipping_Cost"] = sim_df["Shipping_Cost"] * (1 + shipping_cost_increase_pct / 100.0)

    # Recalculate Dependencies
    sim_df["Stock_Cover_Days"] = np.round((sim_df["Current_Stock"] / np.maximum(sim_df["Monthly_Sales_Est"], 1)) * 30, 1)
    sim_df["Stockout_Risk_Flag"] = (sim_df["Stock_Cover_Days"] < sim_df["Supplier_Lead_Time_Days"]).astype(int)

    baseline_health = calculate_health_score(df, active_risks_count=df["Stockout_Risk_Flag"].sum())
    simulated_health = calculate_health_score(sim_df, active_risks_count=sim_df["Stockout_Risk_Flag"].sum())

    stockouts_baseline = int(df["Stockout_Risk_Flag"].sum())
    stockouts_simulated = int(sim_df["Stockout_Risk_Flag"].sum())

    return {
        "parameters": {
            "demand_surge_pct": demand_surge_pct,
            "lead_time_delay_days": lead_time_delay_days,
            "shipping_cost_increase_pct": shipping_cost_increase_pct
        },
        "baseline": {
            "health_score": baseline_health["overall_health_score"],
            "stockout_count": stockouts_baseline
        },
        "simulated": {
            "health_score": simulated_health["overall_health_score"],
            "stockout_count": stockouts_simulated
        },
        "delta": {
            "health_score_change": round(simulated_health["overall_health_score"] - baseline_health["overall_health_score"], 1),
            "additional_stockouts": stockouts_simulated - stockouts_baseline
        }
    }
