
# 🧭 OpenAI to Z Challenge – Discovering Hidden Archaeological Sites in the Amazon

This repository contains the structure and development of the project for the international **OpenAI to Z Challenge**, hosted by Kaggle and OpenAI. The goal is to discover previously undocumented archaeological sites in the Amazon through the use of language models (LLMs), public satellite and LiDAR data, and reproducible scientific methods.

## 📌 Objective

Leverage artificial intelligence, open geospatial data (such as Sentinel-2 and OpenTopography), historical texts, and indigenous maps to:
- **Detect promising locations** with evidence of past civilizations;
- **Generate cross-referenced evidence** from multiple sources (LiDAR, imagery, historical narrative);
- **Suggest plausible geographic coordinates** for new archaeological sites;
- **Support researchers and archaeologists** in advancing the preservation of Amazonian historical heritage.

## 🗂️ Project Structure

```bash
📁 data/           # Collected data (LiDAR, Sentinel-2, Historical Texts)
📁 notebooks/      # Jupyter Notebooks with analyses
📁 src/            # Processing scripts and models
📁 outputs/        # Generated maps, visualizations, evidence
📁 writeup/        # Final document for Kaggle submission
📄 README.md       # This file
```

## 🚀 Initial Steps

- [x] Define initial project structure
- [x] Collect open data sources
- [ ] Develop notebooks for data collection and visualization
- [ ] Process and cross-analyze data
- [ ] Write the final report (`writeup_openai_to_z.md`)

## 📦 Technologies and Tools

- 📡 [Google Earth Engine](https://earthengine.google.com/)
- 🛰️ [Sentinel-2 / ESA](https://sentinels.copernicus.eu/web/sentinel/home)
- 🌳 [OpenTopography (LiDAR)](https://opentopography.org/)
- 🤖 OpenAI (GPT-4.1, o4 mini)
- 🧠 Python, geemap, rasterio, geopandas, matplotlib, scikit-learn, torch, folium, transformers

## ✍️ Contribution

This project is open to scientific and technical collaboration. If you have experience in archaeology, AI, geoprocessing, or South American history, feel free to contribute.

## 📅 Deadline

- Final submission: **June 29, 2025**

## 📚 Initial References

- [OpenAI to Z Challenge - Kaggle Page](https://www.kaggle.com/competitions/openai-to-z-challenge)
- [Reference paper: Peripato et al. (2023)](https://www.science.org/doi/10.1126/science.ade2541)
- [Walker et al. (2023) - PeerJ](https://peerj.com/articles/15137/)
- [OpenTopography - Amazonia LiDAR Tiles](https://opentopography.org)

---

**Uncovering the past with AI – one site at a time. 🌎🧠**

---

## 🧭 Project: OpenAI to Z Challenge – Discovery of Archaeological Sites in the Amazon

### 📁 Project Structure
```
├── data/                  # Downloaded data (LiDAR, Sentinel, Texts)
├── notebooks/             # Jupyter Notebooks with analyses
├── src/                   # Processing scripts and AI
├── outputs/               # Visualizations, maps, evidence
├── writeup/               # Final report for submission
└── README.md
```

---

### 🔍 SECTION 1: Identifying Regions of Interest
- [ ] Map areas with high density of known sites
- [ ] Identify gaps in available geospatial data
- [ ] Extract hydrography, terrain, and vegetation layers
- [ ] Delimit regions based on known archaeological patterns

---

### 🛰️ SECTION 2: Satellite and LiDAR Analysis
- [ ] Download Sentinel-2 tiles (GEE or AWS)
- [ ] Process spectral bands (NDVI, NDWI, Red-Edge)
- [ ] Download LiDAR tiles (OpenTopography)
- [ ] Generate Digital Terrain Models (DTMs)
- [ ] Detect topographic anomalies and geometric patterns

---

### 📚 SECTION 3: Historical and Textual Analysis
- [ ] Collect historical texts (Internet Archive, Library of Congress)
- [ ] Extract geographic entities using LLMs (place names, rivers, villages)
- [ ] Cross-reference texts with spatial layers
- [ ] Identify matches between descriptions and topographic anomalies

---

### 🤖 SECTION 4: AI Models and Classification
- [ ] Apply embeddings to match text with geographic coordinates
- [ ] Use OpenAI models to suggest areas based on textual context
- [ ] Train CNN/ResNet classifiers to detect geoglyphs in imagery
- [ ] Use GPT-4.1 to generate hypotheses and write scientific report sections

---

### ✅ SECTION 5: Cross-Validation and Evidence
- [ ] Compare findings with existing scientific publications (by DOI)
- [ ] Confirm convergence of LiDAR + text + satellite image
- [ ] Mark high-confidence coordinates
- [ ] Generate overlay maps with multiple layers of evidence

---

### 🎬 SECTION 6: Presentation and Submission
- [ ] Create Kaggle Markdown writeup
- [ ] Include public links (Scene ID, Tile ID, DOI)
- [ ] Present reproducible and innovative methods
- [ ] Produce clear visualizations, interactive maps, or videos
- [ ] Test reproducibility with a clear step-by-step

---

### 📦 Tools and Libraries
- geemap, rasterio, geopandas, matplotlib, openai, transformers, scikit-learn, pytorch/keras

---

### 📝 Notes
Each stage can be tracked in version-controlled notebooks within the `notebooks/` folder.  
Recommended: use Hugging Face Spaces or Streamlit for public visualization.

**Focus on compelling evidence, reproducibility, and clarity.**  
**Good luck, digital explorer! 🌎**
