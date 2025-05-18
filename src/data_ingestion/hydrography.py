import os
import geopandas as gpd
import matplotlib.pyplot as plt
import osmnx as ox

# Defina o bounding box (área-alvo) manualmente ou receba como argumento
BBOX = {
    "north": -10.33,
    "south": -10.37,
    "east": -67.13,
    "west": -67.17
}

CACHE_PATH = "data/raw/hydrography/hydrography.geojson"

def download_hydrography(bbox, cache_path):
    if os.path.exists(cache_path):
        print("📂 Cache local encontrado. Carregando dados hidrográficos...")
        gdf = gpd.read_file(cache_path)
    else:
        print("☁️ Baixando dados hidrográficos da OpenStreetMap...")
        # bbox no formato (left, bottom, right, top)
        bbox_tuple = (
            bbox["west"],
            bbox["south"],
            bbox["east"],
            bbox["north"]
        )

        tags = {"waterway": True, "natural": "water"}
        polygon = ox.features_from_bbox(bbox_tuple, tags)
        gdf = polygon[["geometry"]].copy()
        os.makedirs(os.path.dirname(cache_path), exist_ok=True)
        gdf.to_file(cache_path, driver="GeoJSON")
        print(f"✅ Dados salvos em cache: {cache_path}")
    
    return gdf

def plot_hydrography(gdf):
    print("🗺️ Visualizando hidrografia...")
    gdf.plot(figsize=(8, 8), color="blue", linewidth=1)
    plt.title("Corpos d'água e Rios (OpenStreetMap)")
    plt.axis("off")
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    hydro_gdf = download_hydrography(BBOX, CACHE_PATH)
    plot_hydrography(hydro_gdf)
