import os
import tifffile
import numpy as np
import matplotlib.pyplot as plt
from rasterio import open as rio_open
from rasterio.transform import from_origin
from rasterio.enums import Resampling

def gerar_mascara_nuvem(scl_path, output_mask_path, visualizar=False):
    if not os.path.exists(scl_path):
        raise FileNotFoundError(f"Arquivo não encontrado: {scl_path}")
    
    # 🔢 Lê a banda SCL (Scene Classification Layer)
    scl = tifffile.imread(scl_path)

    # 🟧 Define os valores que representam nuvem/sombra
    valores_nuvem = [3, 8, 9]  # 3 = sombra, 8 = nuvem média-alta, 9 = cumulus
    mascara = np.isin(scl, valores_nuvem).astype(np.uint8)  # 1 = nuvem, 0 = limpo

    # 💾 Salva máscara como GeoTIFF
    with rio_open(scl_path) as src:
        meta = src.meta.copy()
        meta.update(dtype="uint8", count=1)

        with rio_open(output_mask_path, "w", **meta) as dst:
            dst.write(mascara, 1)

    print(f"✅ Máscara de nuvem salva em: {output_mask_path}")

    # 👁️ Visualização (opcional)
    if visualizar:
        plt.imshow(mascara, cmap="gray")
        plt.title("Máscara de Nuvem (1 = nuvem)")
        plt.colorbar()
        plt.tight_layout()
        plt.show()

    return mascara

if __name__ == "__main__":
    # Exemplo de caminho da imagem SCL
    center_lat = -10.35
    center_lon = -67.15
    base_name = f"LAT{center_lat:.3f}_LON{center_lon:.3f}".replace("-", "m")
    scl_path = f"data/raw/sentinel2/{base_name}_SCL.tiff"
    mask_path = f"data/raw/sentinel2/{base_name}_CLOUD_MASK.tiff"

    # Gera máscara e salva como GeoTIFF (com visualização para debug)
    gerar_mascara_nuvem(scl_path, mask_path, visualizar=True)
