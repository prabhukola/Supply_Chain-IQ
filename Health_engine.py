def calculate_health_score(df, active_risks_count=0):
    demand_health = max(0, 100 - df["Stockout_Risk_Flag"].mean() * 100)
    
    # Inventory Health: ideal cover is 15-45 days
    cover_penalty = np.where((df["Stock_Cover_Days"] < 15) | (df["Stock_Cover_Days"] > 45), 1, 0).mean() * 100
    inventory_health = max(0, 100 - cover_penalty)

    supplier_health = max(0, 100 - (df["Supplier_Lead_Time_Days"].mean() * 1.5))
    quality_health = max(0, 100 - (df["Defect_Rate_Pct"].mean() * 15))
    logistics_health = max(0, 100 - (df["Shipping_Cost"] / df["Unit_Cost"]).mean() * 200)

    base_score = (
        demand_health * 0.25 +
        inventory_health * 0.25 +
        supplier_health * 0.20 +
        quality_health * 0.15 +
        logistics_health * 0.15
    )

    penalty = active_risks_count * 3.5
    final_score = float(np.clip(base_score - penalty, 0, 100))

    return {
        "overall_health_score": round(final_score, 1),
        "sub_scores": {
            "demand": round(demand_health, 1),
            "inventory": round(inventory_health, 1),
            "supplier": round(supplier_health, 1),
            "quality": round(quality_health, 1),
            "logistics": round(logistics_health, 1)
        },
        "risk_penalty_applied": penalty
    }
