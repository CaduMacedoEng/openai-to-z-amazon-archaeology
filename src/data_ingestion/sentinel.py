from sentinelhub import SHConfig, BBox, CRS, SentinelHubRequest, MimeType, DataCollection, bbox_to_dimensions
import numpy as np
import matplotlib.pyplot as plt
import os
import tifffile
import shutil
import rasterio

def download_rgb_ndvi(center_lat=-10.35, center_lon=-67.15, box_size_km=2):
    config = SHConfig()
    config.sh_client_id = os.getenv("SENTINELHUB_CLIENT_ID")
    config.sh_client_secret = os.getenv("SENTINELHUB_CLIENT_SECRET")

    delta = box_size_km / 111
    bbox_coords = [center_lon - delta, center_lat - delta, center_lon + delta, center_lat + delta]
    bbox = BBox(bbox=bbox_coords, crs=CRS.WGS84)
    size = bbox_to_dimensions(bbox, resolution=10)

    base_name = f"LAT{center_lat:.3f}_LON{center_lon:.3f}".replace("-", "m")
    rgb_cache_path = f"data/raw/sentinel2/{base_name}.tiff"
    scl_cache_path = f"data/raw/sentinel2/{base_name}_SCL.tiff"

    # RGB + NDVI
    if os.path.exists(rgb_cache_path):
        print("📂 Cache RGB/NDVI encontrado.")
        image = tifffile.imread(rgb_cache_path)
    else:
        print("☁️ Baixando RGB + NDVI...")

        evalscript_rgb = """
        function setup() {
          return {
            input: ["B04", "B03", "B02", "B08"],
            output: { bands: 4 }
          };
        }
        function evaluatePixel(sample) {
          let ndvi = index(sample.B08, sample.B04);
          return [sample.B04, sample.B03, sample.B02, ndvi];
        }
        """

        request = SentinelHubRequest(
            data_folder='data/raw/sentinel2/',
            evalscript=evalscript_rgb,
            input_data=[
                SentinelHubRequest.input_data(
                    data_collection=DataCollection.SENTINEL2_L2A,
                    time_interval=('2020-06-01', '2020-09-01'),
                )
            ],
            responses=[SentinelHubRequest.output_response('default', MimeType.TIFF)],
            bbox=bbox,
            size=size,
            config=config
        )

        data = request.get_data(save_data=True)
        image = np.array(data[0])

        base_dir = "data/raw/sentinel2/"
        subdirs = [d for d in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, d))]
        if not subdirs:
            raise RuntimeError("❌ Nenhuma subpasta encontrada com o arquivo response.tiff (RGB).")
        folder = subdirs[-1]
        response_path = os.path.join(base_dir, folder, "response.tiff")
        shutil.move(response_path, rgb_cache_path)
        shutil.rmtree(os.path.join(base_dir, folder))
        print(f"✅ RGB + NDVI salvo como {rgb_cache_path}")

    # SCL
    if not os.path.exists(scl_cache_path):
        print("☁️ Baixando banda SCL...")

        evalscript_scl = """
        function setup() {
          return {
            input: ["SCL"],
            output: { bands: 1 }
          };
        }
        function evaluatePixel(sample) {
          return [sample.SCL];
        }
        """

        request_scl = SentinelHubRequest(
            data_folder='data/raw/sentinel2/',
            evalscript=evalscript_scl,
            input_data=[
                SentinelHubRequest.input_data(
                    data_collection=DataCollection.SENTINEL2_L2A,
                    time_interval=('2020-06-01', '2020-09-01'),
                )
            ],
            responses=[SentinelHubRequest.output_response('default', MimeType.TIFF)],
            bbox=bbox,
            size=size,
            config=config
        )

        data_scl = request_scl.get_data(save_data=True)

        base_dir = "data/raw/sentinel2/"
        subdirs = [d for d in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, d))]
        if not subdirs:
            raise RuntimeError("❌ Nenhuma subpasta encontrada com o arquivo response.tiff (SCL).")
        folder = subdirs[-1]
        scl_path = os.path.join(base_dir, folder, "response.tiff")
        shutil.move(scl_path, scl_cache_path)
        shutil.rmtree(os.path.join(base_dir, folder))
        print(f"✅ Banda SCL salva como {scl_cache_path}")
    else:
        print("📂 Cache da banda SCL encontrado.")

    return image

def normalize_band(band, lower=2, upper=98):
    p_low, p_high = np.percentile(band, (lower, upper))
    return np.clip((band - p_low) / (p_high - p_low), 0, 1)

if __name__ == "__main__":
    image = download_rgb_ndvi(center_lat=-10.35, center_lon=-67.15)

    print("📊 Intervalo RGB:")
    for i, color in enumerate(['R', 'G', 'B']):
        print(f"{color}: {image[:, :, i].min()} → {image[:, :, i].max()}")

    rgb_norm = np.stack([
        normalize_band(image[:, :, 0]),
        normalize_band(image[:, :, 1]),
        normalize_band(image[:, :, 2])
    ], axis=-1)

    plt.figure(figsize=(10, 5))

    plt.subplot(1, 2, 1)
    plt.imshow(rgb_norm)
    plt.title("Sentinel-2 RGB")
    plt.axis("off")

    plt.subplot(1, 2, 2)
    plt.imshow(image[:, :, 3], cmap="RdYlGn")
    plt.colorbar(label="NDVI")
    plt.title("NDVI")
    plt.axis("off")

    plt.tight_layout()
    plt.show()
