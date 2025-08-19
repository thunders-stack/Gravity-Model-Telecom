import csv

# City data with coordinates and population

city_data = [
    {"CityName": "Aachen", "Latitude": 50.76, "Longitude": 6.04, "Population": 252136}, # [2]
    {"CityName": "Augsburg", "Latitude": 48.33, "Longitude": 10.90, "Population": 301033}, # [2]
    {"CityName": "Bayreuth", "Latitude": 49.93, "Longitude": 11.59, "Population": 73074}, # [3]
    {"CityName": "Berlin", "Latitude": 52.52, "Longitude": 13.39, "Population": 3897145}, # [4]
    {"CityName": "Bielefeld", "Latitude": 52.04, "Longitude": 8.50, "Population": 338332}, # [2]
    {"CityName": "Braunschweig", "Latitude": 52.28, "Longitude": 10.55, "Population": 251804}, # [2]
    {"CityName": "Bremen", "Latitude": 53.11, "Longitude": 8.85, "Population": 569396}, # [2]
    {"CityName": "Bremerhaven", "Latitude": 53.54, "Longitude": 8.58, "Population": 117446}, # [5]
    {"CityName": "Chemnitz", "Latitude": 50.84, "Longitude": 12.93, "Population": 248563}, # [2]
    {"CityName": "Darmstadt", "Latitude": 49.89, "Longitude": 8.65, "Population": 162243}, # [2]
    {"CityName": "Dortmund", "Latitude": 51.51, "Longitude": 7.45, "Population": 598246}, # [6]
    {"CityName": "Dresden", "Latitude": 51.03, "Longitude": 13.73, "Population": 563311}, # [2]
    {"CityName": "Duesseldorf", "Latitude": 51.25, "Longitude": 6.77, "Population": 629047}, # [2]
    {"CityName": "Erfurt", "Latitude": 50.98, "Longitude": 11.04, "Population": 218793}, # [7]
    {"CityName": "Essen", "Latitude": 51.46, "Longitude": 7.02, "Population": 584580}, # [2]
    {"CityName": "Flensburg", "Latitude": 54.77, "Longitude": 9.45, "Population": 92550}, # [2]
    {"CityName": "Frankfurt", "Latitude": 50.12, "Longitude": 8.71, "Population": 773068}, # [2]
    {"CityName": "Freiburg", "Latitude": 47.98, "Longitude": 7.80, "Population": 236140}, # [2]
    {"CityName": "Fulda", "Latitude": 50.56, "Longitude": 9.69, "Population": 65735}, # [8]
    {"CityName": "Giessen", "Latitude": 50.57, "Longitude": 8.67, "Population": 90000}, # [9]
    {"CityName": "Greifswald", "Latitude": 54.09, "Longitude": 13.40, "Population": 59000}, # [10]
    {"CityName": "Hamburg", "Latitude": 53.57, "Longitude": 9.99, "Population": 1845229}, # [11]
    {"CityName": "Hannover", "Latitude": 52.38, "Longitude": 9.72, "Population": 545045}, # [2]
    {"CityName": "Kaiserslautern", "Latitude": 49.43, "Longitude": 7.75, "Population": 101228}, # [2]
    {"CityName": "Karlsruhe", "Latitude": 49.01, "Longitude": 8.41, "Population": 308707}, # [2]
    {"CityName": "Kassel", "Latitude": 51.32, "Longitude": 9.51, "Population": 204202}, # [2]
    {"CityName": "Kempten", "Latitude": 47.72, "Longitude": 10.32, "Population": 65933}, # [12]
    {"CityName": "Kiel", "Latitude": 54.34, "Longitude": 10.12, "Population": 247717}, # [2]
    {"CityName": "Koblenz", "Latitude": 50.40, "Longitude": 7.52, "Population": 115268}, # [2]
    {"CityName": "Koeln", "Latitude": 50.94, "Longitude": 6.87, "Population": 1084831}, # [2]
    {"CityName": "Konstanz", "Latitude": 47.66, "Longitude": 9.18, "Population": 81275}, # [13]
    {"CityName": "Leipzig", "Latitude": 51.34, "Longitude": 12.38, "Population": 616093}, # [2]
    {"CityName": "Magdeburg", "Latitude": 52.14, "Longitude": 11.64, "Population": 239364}, # [2]
    {"CityName": "Mannheim", "Latitude": 49.49, "Longitude": 8.49, "Population": 315554}, # [2]
    {"CityName": "Muenchen", "Latitude": 48.15, "Longitude": 11.57, "Population": 2606021}, # [2]
    {"CityName": "Muenster", "Latitude": 51.97, "Longitude": 7.60, "Population": 320946}, # [2]
    {"CityName": "Norden", "Latitude": 53.60, "Longitude": 7.21, "Population": 25179}, # [14]
    {"CityName": "Nuernberg", "Latitude": 49.57, "Longitude": 11.03, "Population": 523026}, # [2]
    {"CityName": "Oldenburg", "Latitude": 53.11, "Longitude": 8.21, "Population": 172830}, # [2]
    {"CityName": "Osnabrueck", "Latitude": 52.28, "Longitude": 8.03, "Population": 167366}, # [2]
    {"CityName": "Passau", "Latitude": 48.57, "Longitude": 13.46, "Population": 50560}, # [15]
    {"CityName": "Regensburg", "Latitude": 49.00, "Longitude": 12.09, "Population": 157443}, # [2]
    {"CityName": "Saarbruecken", "Latitude": 49.23, "Longitude": 7.03, "Population": 181959}, # [2]
    {"CityName": "Schwerin", "Latitude": 53.55, "Longitude": 11.45, "Population": 98596}, # [2]
    {"CityName": "Siegen", "Latitude": 50.91, "Longitude": 8.03, "Population": 102560}, # [2]
    {"CityName": "Stuttgart", "Latitude": 48.74, "Longitude": 9.10, "Population": 2787724}, # [2]
    {"CityName": "Trier", "Latitude": 49.75, "Longitude": 6.68, "Population": 112195}, # [2]
    {"CityName": "Ulm", "Latitude": 48.40, "Longitude": 9.99, "Population": 128928}, # [2]
    {"CityName": "Wesel", "Latitude": 51.39, "Longitude": 6.37, "Population": 61277}, # [16]
    {"CityName": "Wuerzburg", "Latitude": 49.78, "Longitude": 9.97, "Population": 127810} # [2]
    ]

# We input all this data into a .csv file for convenience

csv_file_path = "german_cities.csv"
fieldnames = ["CityNumber", "CityName", "Population", "Latitude", "Longitude"]

with open(csv_file_path, 'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for i, city in enumerate(city_data):
        writer.writerow({
            "CityNumber": i + 1,
            "CityName": city["CityName"],
            "Population": city["Population"],
            "Latitude": city["Latitude"],
            "Longitude": city["Longitude"]
        })


print(f"'{csv_file_path}' created successfully with {len(city_data)} cities.")
