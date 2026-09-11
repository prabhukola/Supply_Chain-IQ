from flask import Blueprint, jsonify
from app.ml.feature_engineering import load_and_preprocess_data
from app.services.health_engine import calculate_health_score
from app.services.risk_engine import analyze_supply_chain_risks

routes_dashboard = Blueprint("routes_dashboard", __name__)

@routes_dashboard.route("/api/dashboard/kpis", methods=["GET"])
def get_kpis():
    df = load_and_preprocess_data()
    risks = analyze_supply_chain_risks(df)
    health = calculate_health_score(df, active_risks_count=risks["active_risk_count"])

    return jsonify({
        "status": "success",
        "kpis": {
            "health_score": health["overall_health_score"],
            "sub_scores": health["sub_scores"],
            "active_risks_count": risks["active_risk_count"],
            "total_capital_exposed_usd": risks["total_financial_exposure_usd"],
            "total_skus_tracked": len(df)
        }
    })
