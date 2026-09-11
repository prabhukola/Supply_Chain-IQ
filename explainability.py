import numpy as np

def explain_sku_prediction(model_result, sku_row_df):
    model = model_result["model"]
    features = model_result["feature_names"]
    
    row_features = sku_row_df[features]
    prediction = float(model.predict(row_features)[0])

    if hasattr(model, "feature_importances_"):
        importances = model.feature_importances_
    else:
        importances = np.abs(model.coef_)
        importances = importances / np.sum(importances)

    contributions = []
    for f, imp in zip(features, importances):
        val = float(row_features[f].values[0])
        # Proxy directional impact for UX explainability
        impact_val = imp * (val / (val + 10.0))
        contributions.append({
            "feature": f,
            "value": val,
            "importance": round(float(imp), 4),
            "estimated_impact": round(float(impact_val), 4)
        })

    contributions = sorted(contributions, key=lambda x: x["importance"], reverse=True)

    return {
        "sku_id": sku_row_df["SKU_ID"].values[0],
        "predicted_demand_pressure": round(prediction, 2),
        "drivers": contributions[:4]
    }
