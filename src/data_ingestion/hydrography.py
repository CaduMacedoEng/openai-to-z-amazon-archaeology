import os
import argparse
import geopandas as gpd
import matplotlib.pyplot as plt
import osmnx as ox
from osmnx._errors import InsufficientResponseError  # ✅ Importação necessária


def generate_bbox(center_lat, center_lon, box_size_km):
    delta = box_size_km / 111  # Aproximação: 1 grau ≈ 111 km
    return {
        "north": center_lat + delta,
        "south": center_lat - delta,
        "east": center_lon + delta,
        "west": center_lon - delta,
    }

def download_hydrography(bbox, cache_path):
    if os.path.exists(cache_path):
        print("📂 Cache local encontrado. Carregando dados hidrográficos...")
        gdf = gpd.read_file(cache_path)
    else:
        print("☁️ Baixando dados hidrográficos da OpenStreetMap...")
        bbox_tuple = (bbox["west"], bbox["south"], bbox["east"], bbox["north"])
        tags = {"waterway": True, "natural": "water"}

        try:
            polygon = ox.features_from_bbox(bbox_tuple, tags)
            gdf = polygon[["geometry"]].copy()
            os.makedirs(os.path.dirname(cache_path), exist_ok=True)
            gdf.to_file(cache_path, driver="GeoJSON")
            print(f"✅ Dados salvos em cache: {cache_path}")
        except InsufficientResponseError:
            print("⚠️ Nenhum dado hidrográfico encontrado nessa região. Retornando vazio.")
            gdf = gpd.GeoDataFrame(geometry=[], crs="EPSG:4326")

    return gdf

def plot_hydrography(gdf):
    if gdf.empty:
        print("🚫 Nenhuma geometria hidrográfica para exibir.")
        return

    print("🗺️ Visualizando hidrografia...")
    gdf.plot(figsize=(8, 8), color="blue", linewidth=1)
    plt.title("Corpos d'água e Rios (OpenStreetMap)")
    plt.axis("off")
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download de hidrografia via OSM")
    parser.add_argument("--lat", type=float, required=True, help="Latitude central da área")
    parser.add_argument("--lon", type=float, required=True, help="Longitude central da área")
    parser.add_argument("--box", type=float, default=2, help="Tamanho do box em km")
    args = parser.parse_args()

    # Gera bounding box com base no centro e tamanho do box
    bbox = generate_bbox(args.lat, args.lon, args.box)

    base_name = f"LAT{args.lat:.3f}_LON{args.lon:.3f}".replace("-", "m")
    cache_path = f"data/raw/hydrography/hydro_{base_name}.geojson"

    hydro_gdf = download_hydrography(bbox, cache_path)
    plot_hydrography(hydro_gdf)
