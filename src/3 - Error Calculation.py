# The Error calculation
import os
import pandas as pd
import numpy as np
from math import sqrt
from sklearn.metrics import mean_absolute_error, mean_squared_error
from scipy.stats import spearmanr

POSSIBLE_FLOW_COLS = ["Flow_Adjusted", "Flow", "Value", "Demand"]

def detect_flow_col(df):
    for col in POSSIBLE_FLOW_COLS:
        if col in df.columns:
            return col
    raise ValueError(f"No recognised flow column found. Available: {list(df.columns)}")

def normalize_predictions(y_true, y_pred, method="median"):
    if method == "median":
        factor = np.median(y_pred) / np.median(y_true) if np.median(y_true) != 0 else 1
    elif method == "mean":
        factor = np.mean(y_pred) / np.mean(y_true) if np.mean(y_true) != 0 else 1
    else:
        factor = 1
    return y_pred / factor, factor

def clean_finite(y_true, y_pred):
    y_true = np.array(y_true, dtype=float)
    y_pred = np.array(y_pred, dtype=float)
    mask = np.isfinite(y_true) & np.isfinite(y_pred)
    return y_true[mask], y_pred[mask]

def calc_metrics(df_val, df_pred, model_name):
    flow_col_pred = detect_flow_col(df_pred)
    df_pred = df_pred[["City1", "City2", flow_col_pred]].rename(columns={flow_col_pred: "Flow_pred"})
    df_pred["Flow_pred"] = pd.to_numeric(df_pred["Flow_pred"], errors="coerce").fillna(0)
    merged = pd.merge(df_val, df_pred, on=["City1", "City2"], how="left")
    merged["Flow_pred"] = merged["Flow_pred"].fillna(0)
    merged["Flow_pred"], scale_factor = normalize_predictions(
        merged["Flow_true"], merged["Flow_pred"], method="median"
    )
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

def validate_and_report(data_dir, result_files, validation_file, out_result_csv):
    # Load validation
    val_path = os.path.join(data_dir, validation_file)
    df_val_full = pd.read_csv(val_path)
    val_flow_col = detect_flow_col(df_val_full)
    df_val = df_val_full[["City1", "City2", val_flow_col]].rename(columns={val_flow_col: "Flow_true"})
    df_val["Flow_true"] = pd.to_numeric(df_val["Flow_true"], errors="coerce").fillna(0)
    results = []
    for model_name, filename in result_files.items():
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
    print("\n=== Error Metrics After Median Scaling ===\n")
    print(results_df.to_string(index=False))
    results_df.to_csv(os.path.join(data_dir, out_result_csv), index=False)
    print(f"✅ Results saved to: {os.path.join(data_dir, out_result_csv)}")

if __name__ == "__main__":
    # Example usage for a single result file (edit as needed)
    data_dir = "project_data"
    result_files = {"Gravity1": "gravity_flows.csv"}
    validation_file = "monthly_demand_matrix.csv"
    out_result_csv = "model_error_metrics_with_scaling.csv"
    validate_and_report(data_dir, result_files, validation_file, out_result_csv)
