# src/scripts/download_all_known_sites.py

import os
import subprocess
import geopandas as gpd

# Caminho do GeoJSON com os geoglifos
GEOJSON_PATH = "data/geojson/geoglifos_known.geojson"
BOX_SIZE_KM = 2

def run_command(script, lat, lon):
    command = [
        "python", script,
        "--lat", str(lat),
        "--lon", str(lon),
        "--box", str(BOX_SIZE_KM)
    ]
    print(f"\n🚀 Executando: {' '.join(command)}")
    subprocess.run(command, check=True)

def main():
    if not os.path.exists(GEOJSON_PATH):
        print(f"❌ Arquivo não encontrado: {GEOJSON_PATH}")
        return

    gdf = gpd.read_file(GEOJSON_PATH)

    for _, row in gdf.iterrows():
        lat = row.geometry.y
        lon = row.geometry.x

        print(f"\n📍 Processando coordenada: lat={lat}, lon={lon}")

        try:
            run_command("src/data_ingestion/sentinel.py", lat, lon)
            run_command("src/data_ingestion/lidar.py", lat, lon)
            run_command("src/data_ingestion/hydrography.py", lat, lon)
        except subprocess.CalledProcessError as e:
            print(f"⚠️ Erro ao executar script para lat={lat}, lon={lon}: {e}")

    print("\n✅ Download completo para todos os pontos do GeoJSON.")

if __name__ == "__main__":
    main()
