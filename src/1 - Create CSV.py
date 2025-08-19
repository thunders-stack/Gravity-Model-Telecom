# Follow the format below to create a CSV file with all the data.

city_data = [
    # {"CityName": "Berlin", "Population": 3664088, "Latitude": 52.52, "Longitude": 13.405, "GDP": 160000}, ...
]

csv_file_path = "country_cities.csv"
fieldnames = ["CityNumber", "CityName", "Population", "Latitude", "Longitude", "GDP"]

with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for i, city in enumerate(city_data):
        # Write row with all specified fields
        row = {
            "CityNumber": i + 1,
            "CityName": city.get("CityName", ""),
            "Population": city.get("Population", ""),
            "Latitude": city.get("Latitude", ""),
            "Longitude": city.get("Longitude", ""),
            "GDP": city.get("GDP", "")
        }
        writer.writerow(row)

print(f"'{csv_file_path}' created successfully with {len(city_data)} cities and GDP included in the columns.")
