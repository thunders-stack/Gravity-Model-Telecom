# This is the master file
from city_csv_maker import create_city_csv
from gdp_gravity_viz import run_gravity_and_plot
from model_error_metrics import validate_and_report

def main():
    # === Step 1: Create cities CSV ===
    city_data = [
        {"CityName": "Berlin", "Population": 3664088, "Latitude": 52.52, "Longitude": 13.405, "GDP": 160000},
        # Add more cities...
    ]
    new_data_folder = "project_data"
    cities_csv = f"{new_data_folder}/german_cities_with_gdp.csv"
    create_city_csv(city_data, cities_csv)

    # === Step 2: Gravity Model + Visualization ===
    shapefile = "data/germany_shapefile.shp"
    flows_csv = f"{new_data_folder}/gravity_flows.csv"
    plot_path = f"{new_data_folder}/gravity_plot.png"
    run_gravity_and_plot(cities_csv, shapefile, flows_csv, plot_path, K=64380.06)

    # === Step 3: Error Calculation ===
    # For a single result file
    result_files = {"Gravity1": "gravity_flows.csv"}
    validation_file = "monthly_demand_matrix.csv"
    out_csv = "model_error_metrics_with_scaling.csv"
    validate_and_report(new_data_folder, result_files, validation_file, out_csv)

if __name__ == "__main__":
    main()

