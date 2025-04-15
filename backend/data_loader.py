import requests
import geopandas as gpd 
from shapely.geometry import shape

def get_buildings():
    url = "https://data.calgary.ca/resource/cchr-krqg.geojson"
    params = {
        "$where": "within_circle(polygon, 51.0447, -114.0631, 500)",  # Approx. 3–4 blocks
        "$limit": 1000
    }

    buildingResponse = requests.get(url, params=params)
    buildingData = buildingResponse.json()

    main_features = [f for f in buildingData["features"] if f["geometry"] and f["geometry"]["type"] == "Polygon"]
    main_gdf = gpd.GeoDataFrame.from_features(main_features, crs="EPSG:4326")

    url_metaData = "https://data.calgary.ca/resource/uc4c-6kbd.geojson"
    metaDataParams = {
        "$where": "within_circle(multipolygon, 51.0447, -114.0631, 500)",  # Approx. 3–4 blocks
        "$limit": 1000
    }
    buildingmetaDataResponse = requests.get(url_metaData, params=metaDataParams)
    buildingMetaData = buildingmetaDataResponse.json()

    extra_features = [f for f in buildingMetaData["features"] if f["geometry"]]
    extra_gdf = gpd.GeoDataFrame.from_features(extra_features, crs="EPSG:4326")

    joined = gpd.sjoin(main_gdf, extra_gdf, how="left", predicate="intersects")
    print(joined)

    buildings = []

    for _, row in joined.iterrows():
        if row.geometry.geom_type != "Polygon":
            continue

        coordinates = [[x, y] for x, y in row.geometry.exterior.coords]

        # Calculate height
        try:
            height = float(row.get("rooftop_elev_z", 0)) - float(row.get("grd_elev_min_z", 0))
        except:
            height = 10

        # You can inspect the row fields by printing once
        print("Row keys:", row.keys())
        print("Example row:", row.to_dict())

        building = {
            "coordinates": coordinates,
            "height": height,
            "struct_id": row.get("struct_id"),
            "stage": row.get("stage"),
            "rooftop_elev_z": row.get("rooftop_elev_z"),
            "grd_elev_min_z": row.get("grd_elev_min_z"),
            "extra": {
                "bldg_code": row.get("bldg_code"),
                "bldg_code_desc": row.get("bldg_code_desc"),
                "shape_area": row.get("shape__area"),
                "shape_length": row.get("shape__length"),
                "obscured": row.get("obscured"),
                "create_dt_utc": row.get("create_dt_utc"),
            }
        }

        buildings.append(building)

    return buildings



def filter_buildings(buildings, rule):
    attr = rule['attribute']
    op = rule['operator']
    value = float(rule['value'])
    ops = {">": lambda x: x > value, "<": lambda x: x < value, "=": lambda x: x == value}

    return [b for b in buildings if ops[op](float(b.get(attr, 0)))]
