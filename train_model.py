import os
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import joblib
import mlflow
import mlflow.sklearn

# ------------------------------------------------------------------
# Point MLflow at the tracking server.
# Inside docker-compose it uses the "mlflow" service hostname.
# Locally it falls back to localhost:5001 (where you'll run the server).
# ------------------------------------------------------------------
mlflow.set_tracking_uri(
    os.environ.get("MLFLOW_TRACKING_URI", "http://127.0.0.1:5001")
)
mlflow.set_experiment("student-marks-training")

df = pd.DataFrame({
    "hours_studied": [2, 4, 6, 8, 10],
    "marks":         [40, 55, 65, 80, 95]
})
X = df[["hours_studied"]]
y = df["marks"]

# ------------------------------------------------------------------
# Everything inside this "with" block is recorded as ONE run in MLflow
# ------------------------------------------------------------------
with mlflow.start_run():
    model = LinearRegression()
    model.fit(X, y)

    preds = model.predict(X)
    mse   = mean_squared_error(y, preds)
    r2    = r2_score(y, preds)

    # Log settings/config used for this training run
    mlflow.log_param("model_type",    "LinearRegression")
    mlflow.log_param("training_rows", len(df))

    # Log numeric results — these show as graphs in the MLflow UI
    mlflow.log_metric("r2",  r2)
    mlflow.log_metric("mse", mse)

    # Store the model itself inside the run — lets you load any past version
    mlflow.sklearn.log_model(model, name="model")

    # Also save locally for the Flask API to use immediately
    joblib.dump(model, "student_model.pkl")

    run_id = mlflow.active_run().info.run_id
    print(f"Training complete — run_id={run_id}, r2={r2:.3f}, mse={mse:.3f}")