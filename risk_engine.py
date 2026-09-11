def analyze_supply_chain_risks(df):
    critical_skus = df[df["Stockout_Risk_Flag"] == 1]
    
    risks = []
    total_exposure = 0.0

    for idx, row in critical_skus.iterrows():
        exposure = float(row["Revenue_Exposure"] * 0.4) # estimated lost revenue factor
        total_exposure += exposure
        
        risks.append({
            "risk_id": f"RISK-{row['SKU_ID']}",
            "sku_id": row["SKU_ID"],
            "supplier_id": row["Supplier_ID"],
            "type": "Stockout Risk",
            "severity": "CRITICAL" if row["Stock_Cover_Days"] < 5 else "HIGH",
            "lead_time_days": int(row["Supplier_Lead_Time_Days"]),
            "cover_days": float(row["Stock_Cover_Days"]),
            "financial_exposure_usd": round(exposure, 2),
            "recommendation": f"Expedite order from supplier {row['Supplier_ID']} or reroute stock."
        })

    return {
        "active_risk_count": len(risks),
        "total_financial_exposure_usd": round(total_exposure, 2),
        "risk_list": risks
    }
