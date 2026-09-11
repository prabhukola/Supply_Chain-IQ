from flask import Blueprint, jsonify, request
from app.ml.feature_engineering import load_and_preprocess_data
from app.services.simulation_engine import run_crisis_simulation

routes_simulation = Blueprint("routes_simulation", __name__)

@routes_simulation.route("/api/simulation/run", methods=["POST"])
def simulate():
    payload = request.get_json() or {}
    demand_surge = float(payload.get("demand_surge_pct", 30.0))
    lead_time_delay = int(payload.get("lead_time_delay_days", 5))
    shipping_increase = float(payload.get("shipping_cost_increase_pct", 15.0))

    df = load_and_preprocess_data()
    res = run_crisis_simulation(df, demand_surge, lead_time_delay, shipping_increase)

    return jsonify({"status": "success", "simulation_results": res})
