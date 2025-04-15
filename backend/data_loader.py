import requests

def get_buildings():
    url = "https://data.calgary.ca/resource/cchr-krqg.geojson"
    params = {
        "$where": "within_circle(polygon, 51.0447, -114.0631, 500)",  # Approx. 3–4 blocks
        "$limit": 1000
    }

    response = requests.get(url, params=params)
    data = response.json()

    buildings = []

    for feature in data.get("features", []):
        geom = feature.get("geometry", {})
        props = feature.get("properties", {})

        if geom.get("type") != "Polygon":
            continue

        coordinates = [[float(x), float(y)] for x, y in geom["coordinates"][0]]

        # Compute height if possible
        try:
            height = float(props["rooftop_elev_z"]) - float(props["grd_elev_min_z"])
        except (KeyError, ValueError):
            height = 10

        building = {
            "coordinates": coordinates,
            "height": height,
            "struct_id": props.get("struct_id"),
            "stage": props.get("stage"),
            "rooftop_elev_z": props.get("rooftop_elev_z"),
            "grd_elev_min_z": props.get("grd_elev_min_z"),
        }

        buildings.append(building)

    return buildings



def filter_buildings(buildings, rule):
    attr = rule['attribute']
    op = rule['operator']
    value = float(rule['value'])
    ops = {">": lambda x: x > value, "<": lambda x: x < value, "=": lambda x: x == value}

    return [b for b in buildings if ops[op](float(b.get(attr, 0)))]
