from flask import Blueprint, jsonify, request
from app.ml.feature_engineering import load_and_preprocess_data
from app.services.optimizer_engine import optimize_order_quantities

routes_optimization = Blueprint("routes_optimization", __name__)

@routes_optimization.route("/api/optimization/run", methods=["POST"])
def optimize():
    payload = request.get_json() or {}
    budget = float(payload.get("budget", 150000))
    capacity = int(payload.get("capacity", 10000))

    df = load_and_preprocess_data()
    res = optimize_order_quantities(df, total_budget=budget, max_capacity_units=capacity)

    return jsonify({"status": "success", "optimization": res})
