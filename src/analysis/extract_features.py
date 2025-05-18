import os
import numpy as np
import rasterio
import geopandas as gpd
from rasterio.mask import mask
from scipy.ndimage import distance_transform_edt
import pandas as pd
import glob


def extract_ndvi_features(ndvi_path, cloud_mask_path):
    with rasterio.open(ndvi_path) as src:
        ndvi = src.read(1)
    if os.path.exists(cloud_mask_path):
        with rasterio.open(cloud_mask_path) as src:
            cloud_mask = src.read(1)
        ndvi = np.where(cloud_mask == 1, np.nan, ndvi)
    return np.nanmean(ndvi), np.nanstd(ndvi)


def extract_dtm_features(dtm_path):
    with rasterio.open(dtm_path) as src:
        elevation = src.read(1)
    slope = np.gradient(elevation.astype('float32'))
    slope_magnitude = np.sqrt(slope[0] ** 2 + slope[1] ** 2)
    return np.nanmean(slope_magnitude), np.nanmax(slope_magnitude)


def distance_to_nearest_river(hydro_path, dtm_path):
    with rasterio.open(dtm_path) as src:
        dtm = src.read(1)
        transform = src.transform
        height, width = dtm.shape

    hydro = gpd.read_file(hydro_path).to_crs("EPSG:4326")
    mask_array = np.ones((height, width), dtype=bool)

    for geom in hydro.geometry:
        if geom.is_empty:
            continue

        coords_to_mark = []

        if geom.geom_type == "LineString":
            coords_to_mark = geom.coords
        elif geom.geom_type == "MultiLineString":
            for line in geom:
                coords_to_mark.extend(line.coords)

        for x, y in coords_to_mark:
            try:
                row, col = src.index(x, y)
                if 0 <= row < height and 0 <= col < width:
                    mask_array[row, col] = 0
            except Exception:
                continue  # ignora erros de projeção ou coordenadas inválidas

    dist = distance_transform_edt(mask_array) * abs(transform.a)
    return np.nanmin(dist)


def main():
    geojson_path = "data/geojson/geoglifos_known.geojson"
    dtm_folder = "data/raw/lidar"
    sentinel_folder = "data/raw/sentinel2"
    hydro_folder = "data/raw/hydrography"

    gdf = gpd.read_file(geojson_path)
    feature_rows = []

    for _, row in gdf.iterrows():
        lon, lat = row.geometry.x, row.geometry.y
        base_name = f"LAT{lat:.3f}_LON{lon:.3f}".replace("-", "m")

        ndvi_path = os.path.join(sentinel_folder, f"{base_name}.tiff")
        cloud_mask_path = os.path.join(sentinel_folder, f"{base_name}_CLOUD_MASK.tiff")
        dtm_path = os.path.join(dtm_folder, f"DTM_{base_name}.tif")
        hydro_path = os.path.join(hydro_folder, f"hydro_{base_name}.geojson")

        if not (os.path.exists(ndvi_path) and os.path.exists(dtm_path)):
            print(f"❌ Dados ausentes para {base_name}, pulando...")
            continue

        print(f"✅ Processando {base_name}...")
        ndvi_mean, ndvi_std = extract_ndvi_features(ndvi_path, cloud_mask_path)
        slope_mean, slope_max = extract_dtm_features(dtm_path)
        dist_river = distance_to_nearest_river(hydro_path, dtm_path) if os.path.exists(hydro_path) else np.nan

        feature_rows.append({
            "lat": lat,
            "lon": lon,
            "ndvi_mean": ndvi_mean,
            "ndvi_std": ndvi_std,
            "slope_mean": slope_mean,
            "slope_max": slope_max,
            "dist_river": dist_river,
            "label": 1
        })

    df = pd.DataFrame(feature_rows)
    os.makedirs("data/processed", exist_ok=True)
    df.to_csv("data/processed/features_labeled.csv", index=False)
    print("\n💾 Features salvas em: data/processed/features_labeled.csv")


if __name__ == "__main__":
    main()
