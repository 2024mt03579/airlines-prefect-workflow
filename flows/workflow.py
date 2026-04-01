# To run the file in terminal type > python workflow.py 
# Has to connect with Prefect cloud -> https://app.prefect.cloud/
# Prefect Login [Prefect Cloud] - https://www.prefect.io/opensource  -> get started

# Step 1: Import Required Libraries
import os
import pandas as pd
import numpy as np
from pathlib import Path
from prefect import flow, task
from sklearn.preprocessing import MinMaxScaler

# Step 2: Load the Dataset
@task
def load_dataset():
    # Load the airline dataset from GitHub
    base_dir = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(base_dir, "US_DOT_Airfare_Historical_2008_2025.csv")
    return pd.read_csv(path, low_memory=False)

# Step 3: Data Preprocessing
@task(log_prints=True)
def preprocess_data(df):
    # Print columns with missing values and their count
    missing_values = df.isna().sum()
    columns_with_missing = missing_values[missing_values > 0]
    print("Columns with missing values: ")
    print(columns_with_missing)

    numeric_columns = [
        "year",
        "quarter",
        "distance_miles",
        "passengers",
        "avg_fare",
        "largest_carrier_market_share",
        "largest_carrier_fare",
        "lowest_fare_carrier_share",
        "lowest_fare",
        "fare_per_mile",
    ]

    for column in numeric_columns:
        df[column] = pd.to_numeric(df[column], errors="coerce")

    # Replace missing numeric values with median
    df[numeric_columns] = df[numeric_columns].fillna(df[numeric_columns].median())

    # Discretization by Distance Binning (distance_miles)
    min_value = df["distance_miles"].min()
    max_value = df["distance_miles"].max()
    print("Minimum distance_miles:", min_value)
    print("Maximum distance_miles:", max_value)

    bins = np.linspace(min_value, max_value, 5)
    labels = ["Very Short", "Short", "Medium", "Long"]
    df["bins_dist"] = pd.cut(df["distance_miles"], bins=bins, labels=labels, include_lowest=True)

    print("Distance bin edges:", bins)
    print("Distance bins sample:")
    print(df["bins_dist"].head())

    # One-Hot Encoding for quarter values
    print("One Hot Encoding...")
    quarter_map = {1: "Q1", 2: "Q2", 3: "Q3", 4: "Q4"}
    df["quarter_encoded"] = df["quarter"].astype(int).map(quarter_map)
    print(df["quarter_encoded"].value_counts())

    one_hot_encoded_data = pd.get_dummies(df, columns=["quarter_encoded"], dtype=int)
    quarter_encoded_columns = [column for column in one_hot_encoded_data.columns if column.startswith("quarter_encoded_")]
    print("Quarter encoded columns:", quarter_encoded_columns)

    # Normalize using Min-Max Scaling
    scaler = MinMaxScaler()
    features = df[numeric_columns].drop("avg_fare", axis=1)  # Exclude target variable
    df_normalized = pd.DataFrame(scaler.fit_transform(features), columns=features.columns)
    df_normalized["avg_fare"] = df["avg_fare"]  # Add the target variable back
    df_normalized["bins_dist"] = df["bins_dist"].astype(str)
    df_normalized = pd.concat([df_normalized, one_hot_encoded_data[quarter_encoded_columns]], axis=1)

    # Print the normalized dataframe
    print("Normalized DataFrame:")
    print(df_normalized.head())  # Printing only the first few rows for brevity

    return df_normalized

@task(log_prints=True)
def compute_pearson_analysis(df):
    from scipy.stats import pearsonr
    from matplotlib import pyplot as plt

    feature_x = pd.to_numeric(df["largest_carrier_fare"], errors="coerce")
    feature_y = pd.to_numeric(df["avg_fare"], errors="coerce")
    valid_rows = pd.DataFrame({"largest_carrier_fare": feature_x, "avg_fare": feature_y}).dropna()

    corr, p_value = pearsonr(valid_rows["largest_carrier_fare"], valid_rows["avg_fare"])
    print(f"Pearson correlation (largest_carrier_fare vs avg_fare): {corr:.3f}")
    print(f"p-value: {p_value:.6f}")

    abs_corr = abs(corr)
    if abs_corr < 0.20:
        strength = "very weak"
    elif abs_corr < 0.40:
        strength = "weak"
    elif abs_corr < 0.60:
        strength = "moderate"
    elif abs_corr < 0.80:
        strength = "strong"
    else:
        strength = "very strong"

    direction = "positive" if corr >= 0 else "negative"
    print(f"Interpretation: {strength} {direction} correlation between largest_carrier_fare and avg_fare.")

    output_dir = Path(__file__).resolve().parent.parent / "output"
    output_dir.mkdir(parents=True, exist_ok=True)
    scatter_plot_path = output_dir / "pearson_scatter_airline.png"

    plt.figure(figsize=(8, 5))
    plt.scatter(valid_rows["largest_carrier_fare"], valid_rows["avg_fare"], alpha=0.4)
    plt.title("largest_carrier_fare vs avg_fare")
    plt.xlabel("largest_carrier_fare")
    plt.ylabel("avg_fare")
    plt.tight_layout()
    plt.savefig(scatter_plot_path)
    plt.close()

    print(f"Scatter plot saved to: {scatter_plot_path}")
    return {"pearson_correlation": corr, "p_value": p_value, "scatter_plot": str(scatter_plot_path)}


@task(log_prints=True)
def compute_feature_importance(df):
    from matplotlib import pyplot as plt
    from sklearn.ensemble import RandomForestRegressor

    numeric_df = df.select_dtypes(include=["number"]).copy()
    X = numeric_df.drop("avg_fare", axis=1)
    y = numeric_df["avg_fare"]

    model = RandomForestRegressor(n_estimators=200, random_state=42, n_jobs=-1)
    model.fit(X, y)

    importance_df = (
        pd.DataFrame({"feature": X.columns, "importance": model.feature_importances_})
        .sort_values("importance", ascending=False)
        .reset_index(drop=True)
    )
    top_features = importance_df.head(10)
    print("Top 10 feature importances:")
    print(top_features)

    output_dir = Path(__file__).resolve().parent.parent / "output"
    output_dir.mkdir(parents=True, exist_ok=True)
    csv_path = output_dir / "feature_importance_airline.csv"
    plot_path = output_dir / "feature_importance_airline_top10.png"

    importance_df.to_csv(csv_path, index=False)

    plt.figure(figsize=(10, 6))
    plt.barh(top_features["feature"][::-1], top_features["importance"][::-1])
    plt.title("Top 10 Feature Importances for avg_fare")
    plt.xlabel("Importance")
    plt.ylabel("Feature")
    plt.tight_layout()
    plt.savefig(plot_path)
    plt.close()

    print(f"Feature importance CSV saved to: {csv_path}")
    print(f"Feature importance plot saved to: {plot_path}")
    return {
        "top_features": top_features.to_dict(orient="records"),
        "importance_csv": str(csv_path),
        "importance_plot": str(plot_path),
    }


@task(log_prints=True)
def generate_univariate_visualizations(df):
    from matplotlib import pyplot as plt

    avg_fare_series = pd.to_numeric(df["avg_fare"], errors="coerce").dropna()

    output_dir = Path(__file__).resolve().parent.parent / "output"
    output_dir.mkdir(parents=True, exist_ok=True)
    hist_path = output_dir / "univariate_hist_avg_fare.png"
    box_path = output_dir / "univariate_box_avg_fare.png"

    plt.figure(figsize=(8, 5))
    plt.hist(avg_fare_series, bins=30, alpha=0.8)
    plt.title("Univariate Histogram: avg_fare")
    plt.xlabel("avg_fare")
    plt.ylabel("Frequency")
    plt.tight_layout()
    plt.savefig(hist_path)
    plt.close()

    plt.figure(figsize=(8, 4))
    plt.boxplot(avg_fare_series, vert=False)
    plt.title("Univariate Boxplot: avg_fare")
    plt.xlabel("avg_fare")
    plt.tight_layout()
    plt.savefig(box_path)
    plt.close()

    print(f"Univariate histogram saved to: {hist_path}")
    print(f"Univariate boxplot saved to: {box_path}")
    return {"histogram": str(hist_path), "boxplot": str(box_path)}

# Step 4: Model Training
@task
def train_model(df):
    # Train regression models to predict average fare
    from sklearn.model_selection import train_test_split
    from sklearn.linear_model import LinearRegression, Ridge
    from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score, mean_absolute_percentage_error
    
    X = df.drop("avg_fare", axis=1)
    X = X.select_dtypes(include=["number"])
    y = df["avg_fare"]
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    models = {
        "linear_regression": LinearRegression(),
        "ridge_regression": Ridge(alpha=1.0),
    }

    model_metrics = {}
    for model_name, model in models.items():
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)

        mae = mean_absolute_error(y_test, y_pred)
        rmse = mean_squared_error(y_test, y_pred) ** 0.5
        r2 = r2_score(y_test, y_pred)
        mape = mean_absolute_percentage_error(y_test, y_pred)

        model_metrics[model_name] = {
            "mae": mae,
            "rmse": rmse,
            "r2": r2,
            "mape": mape,
        }

    best_model_name = min(model_metrics, key=lambda name: model_metrics[name]["rmse"])

    return {
        "split": {"train": 0.7, "test": 0.3},
        "models": model_metrics,
        "best_model_by_rmse": best_model_name,
    }

# Step 5: Define Prefect Flow
@flow(log_prints=True)
def workflow_Airline_DataSet():
    # step 1 = loading data
    data = load_dataset()
    # step 2 = pearson correlation analysis
    pearson_stats = compute_pearson_analysis(data)
    print("Pearson Stats:", pearson_stats)
    # step 3 = preprocessing
    preprocessed_data = preprocess_data(data)
    # step 4 = feature importance (explicit EDA requirement)
    feature_importance_stats = compute_feature_importance(preprocessed_data)
    print("Feature Importance Stats:", feature_importance_stats)
    # step 5 = univariate visualization (explicit EDA requirement)
    univariate_plots = generate_univariate_visualizations(data)
    print("Univariate Visualization Paths:", univariate_plots)
    # step 6 = data modeling
    metrics = train_model(preprocessed_data)

    print("Model Metrics:", metrics)
   
# Step 6: Run the Prefect Flow
if __name__ == "__main__":
    #workflow_Airline_DataSet.serve(name="airline-dataset-workflow",
    #                  tags=["first workflow"],
    #                  parameters={},
    #                  interval=120) #2 minutes
    workflow_Airline_DataSet()
