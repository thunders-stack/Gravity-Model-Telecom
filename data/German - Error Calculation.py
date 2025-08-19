import os
import pandas as pd
import numpy as np
from math import sqrt
from sklearn.metrics import mean_absolute_error, mean_squared_error
from scipy.stats import spearmanr

# ===== CONFIG =====
data_dir = r"C:\Users\D\Desktop\CDAC\.venv\Project Data\Germany - Daily"

files = {
    'Gravity1': 'gravity_flows_dist1.csv',
    'Gravity2': 'germany_gravity_flows.csv',
    'Gravity3': 'germany_gravity_flows_distsq.csv',
    'Gravity4': 'germany_gravity_flows_gdpc_distsq.csv',
    'Gravity5': 'gravity_fitted_calls.csv',
    'Gravity6': 'gravity_flows_dist2.csv',
}

validation_file = 'monthly_demand_matrix.csv'

# Possible flow column names we will look for
possible_flow_cols = ["Flow_Adjusted", "Flow", "Value", "Demand"]

# ===== FUNCTIONS =====
def detect_flow_col(df):
    """Find first matching flow column from possible names."""
    for col in possible_flow_cols:
        if col in df.columns:
            return col
    raise ValueError(f"No recognised flow column found. Available: {list(df.columns)}")

def normalize_predictions(y_true, y_pred, method="median"):
    """Scale predictions to match the scale of validation data."""
    if method == "median":
        factor = np.median(y_pred) / np.median(y_true) if np.median(y_true) != 0 else 1
    elif method == "mean":
        factor = np.mean(y_pred) / np.mean(y_true) if np.mean(y_true) != 0 else 1
    else:
        factor = 1
    return y_pred / factor, factor

def clean_finite(y_true, y_pred):
    """Remove NaN/Inf values from both arrays before metrics."""
    y_true = np.array(y_true, dtype=float)
    y_pred = np.array(y_pred, dtype=float)
    mask = np.isfinite(y_true) & np.isfinite(y_pred)
    return y_true[mask], y_pred[mask]

def calc_metrics(df_val, df_pred, model_name):
    """Calculate all error metrics after merging and scaling."""
    # Detect and rename flow columns
    flow_col_pred = detect_flow_col(df_pred)
    df_pred = df_pred[["City1", "City2", flow_col_pred]].rename(columns={flow_col_pred: "Flow_pred"})
    df_pred["Flow_pred"] = pd.to_numeric(df_pred["Flow_pred"], errors="coerce").fillna(0)

    merged = pd.merge(df_val, df_pred, on=["City1", "City2"], how="left")
    merged["Flow_pred"] = merged["Flow_pred"].fillna(0)

    # Scale predictions to match validation median
    merged["Flow_pred"], scale_factor = normalize_predictions(
        merged["Flow_true"], merged["Flow_pred"], method="median"
    )

    # Metric calculations with cleaned data
    y_true, y_pred = clean_finite(merged["Flow_true"], merged["Flow_pred"])

    mae = mean_absolute_error(y_true, y_pred)
    rmse = sqrt(mean_squared_error(y_true, y_pred))

    mask = y_true != 0
    mape = np.mean(np.abs((y_true[mask] - y_pred[mask]) / y_true[mask])) * 100 if mask.any() else np.nan
    smape = np.mean(2 * np.abs(y_true - y_pred) / (np.abs(y_true) + np.abs(y_pred) + 1e-9)) * 100
    mdae = np.median(np.abs(y_true - y_pred))
    denom = sqrt(np.mean(y_true**2)) + sqrt(np.mean(y_pred**2))
    theil_u = rmse / denom if denom != 0 else np.nan
    pearson_r = np.corrcoef(y_true, y_pred)[0, 1] if len(y_true) > 1 else np.nan
    spearman_rho = spearmanr(y_true, y_pred).correlation if len(y_true) > 1 else np.nan

    return {
        "Model": model_name,
        "ScalingFactor": scale_factor,
        "MAE": mae,
        "RMSE": rmse,
        "MAPE(%)": mape,
        "sMAPE(%)": smape,
        "MdAE": mdae,
        "Theil_U": theil_u,
        "Pearson_r": pearson_r,
        "Spearman_rho": spearman_rho
    }

# ===== MAIN SCRIPT =====
if __name__ == "__main__":
    # Load validation file
    val_path = os.path.join(data_dir, validation_file)
    df_val_full = pd.read_csv(val_path)
    val_flow_col = detect_flow_col(df_val_full)

    df_val = df_val_full[["City1", "City2", val_flow_col]].rename(columns={val_flow_col: "Flow_true"})
    df_val["Flow_true"] = pd.to_numeric(df_val["Flow_true"], errors="coerce").fillna(0)

    results = []
    for model_name, filename in files.items():
        file_path = os.path.join(data_dir, filename)
        if not os.path.isfile(file_path):
            print(f"⚠ File not found for {model_name} -> {filename}")
            continue

        df_pred_full = pd.read_csv(file_path)
        try:
            metrics = calc_metrics(df_val, df_pred_full, model_name)
            results.append(metrics)
        except Exception as e:
            print(f"❌ Error processing {model_name}: {e}")

    results_df = pd.DataFrame(results)
    pd.set_option("display.float_format", "{:,.6f}".format)

    print("\n=== Error Metrics After Median Scaling ===\n")
    print(results_df.to_string(index=False))

    # Save results to CSV
    out_path = os.path.join(data_dir, "model_error_metrics_with_scaling.csv")
    results_df.to_csv(out_path, index=False)
    print(f"\n✅ Results saved to: {out_path}")
