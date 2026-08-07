
import csv

def export_to_csv(results, filename="results.csv"):
    with open(filename, "w", newline="", encoding="utf-8-sig") as file:
        writer = csv.writer(file)

        writer.writerow([
            "Name",
            "Address",
            "Latitude",
            "Longitude",
            "Google Maps"
        ])

        for row in results:
            writer.writerow([
                row.get("name", ""),
                row.get("address", ""),
                row.get("lat", ""),
                row.get("lon", ""),
                row.get("link", "")
            ])

    return filename
