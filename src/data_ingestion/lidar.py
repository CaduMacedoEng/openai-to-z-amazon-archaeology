
import os
import numpy as np
import rasterio
import requests
import argparse

def download_dtm(center_lat=-10.35, center_lon=-67.15, box_size_km=2):
    api_key = os.getenv("OPENTOPO_API_KEY")
    if not api_key:
        raise ValueError("❌ API Key da OpenTopography não encontrada no ambiente!")

    delta = box_size_km / 111
    min_lat = center_lat - delta
    max_lat = center_lat + delta
    min_lon = center_lon - delta
    max_lon = center_lon + delta

    bbox_str = f"{min_lon},{min_lat},{max_lon},{max_lat}"
    filename = f"DTM_LAT{center_lat:.3f}_LON{center_lon:.3f}".replace("-", "m") + ".tif"
    output_path = f"data/raw/lidar/{filename}"

    if os.path.exists(output_path):
        print("📂 DTM já existe em cache:", output_path)
        return output_path

    print("☁️ DTM não encontrado localmente. Requisitando da OpenTopography API...")

    url = (
        "https://portal.opentopography.org/API/globaldem?"
        f"demtype=SRTMGL1&south={min_lat}&north={max_lat}&west={min_lon}&east={max_lon}"
        f"&outputFormat=GTiff&API_Key={api_key}"
    )

    response = requests.get(url, stream=True)
    if response.status_code != 200:
        raise RuntimeError(f"❌ Falha ao baixar DTM: {response.status_code} - {response.text}")

    with open(output_path, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)

    print("✅ DTM salvo em cache:", output_path)

    with rasterio.open(output_path) as src:
        print("📍 Bounding Box do DTM:")
        print(f" - Left:   {src.bounds.left}")
        print(f" - Bottom: {src.bounds.bottom}")
        print(f" - Right:  {src.bounds.right}")
        print(f" - Top:    {src.bounds.top}")
        print("🌐 CRS (Sistema de Coordenadas):", src.crs)

    return output_path

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Baixar DTM com OpenTopography")
    parser.add_argument("--lat", type=float, required=True, help="Latitude central da área")
    parser.add_argument("--lon", type=float, required=True, help="Longitude central da área")
    parser.add_argument("--box", type=float, default=2, help="Tamanho da área em km")

    args = parser.parse_args()
    download_dtm(center_lat=args.lat, center_lon=args.lon, box_size_km=args.box)
