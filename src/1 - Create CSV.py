# This acts as the script to create an input file.
import csv

def create_city_csv(city_data, csv_file_path):
    fieldnames = ["CityNumber", "CityName", "Population", "Latitude", "Longitude", "GDP"]
    with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for i, city in enumerate(city_data):
            row = {
                "CityNumber": i + 1,
                "CityName": city.get("CityName", ""),
                "Population": city.get("Population", ""),
                "Latitude": city.get("Latitude", ""),
                "Longitude": city.get("Longitude", ""),
                "GDP": city.get("GDP", "")
            }
            writer.writerow(row)
    print(f"[csv_maker] Created '{csv_file_path}' with {len(city_data)} cities.")

if __name__ == "__main__":
    # Example usage for direct script run, typically not needed when using as a module
    city_data = [
        {"CityName": "Berlin", "Population": 3664088, "Latitude": 52.52, "Longitude": 13.405, "GDP": 160000}
    ]
    create_city_csv(city_data, "project_data/country_cities.csv")
