import numpy as np
import pandas as pd
from sklearn.model_selection import KFold
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.linear_model import Ridge
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor

def train_demand_pressure_models(df):
    features = [
        "Unit_Cost", "Current_Stock", "Monthly_Sales_Est", 
        "Supplier_Lead_Time_Days", "Defect_Rate_Pct", "Shipping_Cost", "Stock_Cover_Days"
    ]
    target = "Demand_Pressure_Index"

    X = df[features]
    y = df[target]

    models = {
        "Ridge": Ridge(alpha=1.0),
        "RandomForest": RandomForestRegressor(n_estimators=50, random_state=42),
        "XGBoost": XGBRegressor(n_estimators=50, max_depth=3, learning_rate=0.1, random_state=42)
    }

    kf = KFold(n_splits=5, shuffle=True, random_state=42)
    performance = {}
    best_model_name = None
    best_score = float("inf")
    best_model_obj = None

    for name, model in models.items():
        rmse_scores = []
        r2_scores = []
        for train_idx, test_idx in kf.split(X):
            X_train, X_test = X.iloc[train_idx], X.iloc[test_idx]
            y_train, y_test = y.iloc[train_idx], y.iloc[test_idx]

            model.fit(X_train, y_train)
            preds = model.predict(X_test)
            
            rmse_scores.append(np.sqrt(mean_squared_error(y_test, preds)))
            r2_scores.append(r2_score(y_test, preds))

        avg_rmse = float(np.mean(rmse_scores))
        avg_r2 = float(np.mean(r2_scores))
        
        performance[name] = {"RMSE": round(avg_rmse, 4), "R2": round(avg_r2, 4)}

        if avg_rmse < best_score:
            best_score = avg_rmse
            best_model_name = name
            best_model_obj = model

    # Retrain best model on full dataset
    best_model_obj.fit(X, y)

    return {
        "performance_comparison": performance,
        "best_model_name": best_model_name,
        "model": best_model_obj,
        "feature_names": features
    }
