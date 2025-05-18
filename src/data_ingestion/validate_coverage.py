import os
import tifffile
import numpy as np

def validar_imagem(path_rgb_ndvi, path_cloud_mask, limiar_nuvem=0.5, limiar_ndvi=5):
    """
    Avalia a cobertura e a qualidade da imagem Sentinel-2.
    
    - limiar_nuvem: fração máxima de pixels nublados permitida (0.5 = 50%)
    - limiar_ndvi: valor mínimo médio de NDVI para ser considerado válido (>5 típico)
    """
    if not os.path.exists(path_rgb_ndvi):
        return f"❌ Arquivo NDVI ausente: {path_rgb_ndvi}"
    
    if not os.path.exists(path_cloud_mask):
        return f"❌ Máscara de nuvem ausente: {path_cloud_mask}"
    
    ndvi = tifffile.imread(path_rgb_ndvi)[:, :, 3]
    cloud_mask = tifffile.imread(path_cloud_mask)

    # Verificações
    if np.all(ndvi == 0):
        return "❌ NDVI todo zerado"
    
    if np.all(np.isnan(ndvi)):
        return "❌ NDVI todo NaN"

    cloud_fraction = cloud_mask.sum() / cloud_mask.size
    mean_ndvi = np.mean(ndvi[~np.isnan(ndvi)])

    if cloud_fraction > limiar_nuvem:
        return f"⚠️ Muita nuvem: {cloud_fraction:.1%}"

    if mean_ndvi < limiar_ndvi:
        return f"⚠️ NDVI baixo: média = {mean_ndvi:.2f}"

    return "✅ Qualidade aceitável"

if __name__ == "__main__":
    from glob import glob

    root = "data/raw/sentinel2"
    imagens = sorted([f for f in os.listdir(root) if f.endswith(".tiff") and "_SCL" not in f and "_CLOUD" not in f])

    print(f"🔍 Validando {len(imagens)} arquivos Sentinel-2...\n")
    for img_name in imagens:
        base = img_name.replace(".tiff", "")
        path_ndvi = os.path.join(root, img_name)
        path_mask = os.path.join(root, f"{base}_CLOUD_MASK.tiff")

        resultado = validar_imagem(path_ndvi, path_mask)
        print(f"{img_name:40s} -> {resultado}")
