from flask import Blueprint, jsonify, request
from app.ml.feature_engineering import load_and_preprocess_data
from app.ml.model_trainer import train_demand_pressure_models
from app.ml.explainability import explain_sku_prediction

routes_demand = Blueprint("routes_demand", __name__)

@routes_demand.route("/api/demand/ml-summary", methods=["GET"])
def get_ml_summary():
    df = load_and_preprocess_data()
    trainer_results = train_demand_pressure_models(df)

    sku_id = request.args.get("sku_id", default=df["SKU_ID"].iloc[0])
    sku_row = df[df["SKU_ID"] == sku_id]

    explanation = {}
    if not sku_row.empty:
        explanation = explain_sku_prediction(trainer_results, sku_row)

    return jsonify({
        "status": "success",
        "best_model": trainer_results["best_model_name"],
        "cross_validation": trainer_results["performance_comparison"],
        "explanation": explanation
    })
