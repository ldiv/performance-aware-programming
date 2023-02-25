import json
import random
from itertools import count


N = 10_000_000

CITIES_PATH = "data/cities.json"
COUNTRIES_PATH = "data/countries.json"
OUTPUT_PATH = "data/data_10000000_flex.json"


def _load_cities():
    with open(CITIES_PATH) as f:
        return json.load(f)


def _load_countries(cities):
    with open(COUNTRIES_PATH) as f:
        country_data = json.load(f)
        countries = {}
        for entry in country_data:
            countries[entry["name"]] = {"region": entry["region"], "cities": []}

        for city in cities:
            countries[city["country_name"]]["cities"].append(city)
        return countries


def run():
    cities = _load_cities()
    countries = _load_countries(cities)

    with open(OUTPUT_PATH, "w") as f:
        routes = []
        for _ in count():
            country_from = random.choice(list(countries.keys()))
            country_to = random.choice(list(countries.keys()))
            if not countries[country_from].get("cities") or not countries[country_to].get("cities"):
                continue
            city_from = random.choice(countries[country_from]["cities"])
            city_to = random.choice(countries[country_to]["cities"])

            routes.append({
                "x0": float(city_from["latitude"]),
                "x1": float(city_from["longitude"]),
                "y0": float(city_to["latitude"]),
                "y1": float(city_to["longitude"]),
            })

            if len(routes) >= N:
                break

        f.write(json.dumps({"pairs": routes}, indent=4))

run()
