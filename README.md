# 🌱 Precision Weed Detection and Targeted Spraying

## 📌 Project Overview

This project develops a **geospatial precision agriculture workflow** to identify potential weed-prone zones using **Sentinel-2 satellite imagery and NDVI analysis**, and to generate **targeted spraying management maps**.

The goal is to support **site-specific weed management**, reducing unnecessary herbicide application and improving sustainability.

---

## 🎯 Objectives

* Analyze vegetation health using remote sensing data
* Detect spatial variability in crop conditions
* Identify **potential weed-prone / low-vigor zones**
* Convert raster outputs into **actionable management zones**
* Generate a **spray priority map** for decision-making

---

## 🧠 Key Concept

Instead of spraying the entire field:

👉 Detect **where intervention is needed**
👉 Spray only those specific zones

This approach enables:

* Reduced chemical usage
* Cost optimization
* Environmental protection
* Data-driven farming decisions

---

## 🗂️ Project Workflow

```
Satellite Data (Sentinel-2)
        ↓
Preprocessing (AOI + Filtering)
        ↓
NDVI Calculation
        ↓
Vegetation Classification
        ↓
Weak Zone Detection
        ↓
Weed Suspicion Mapping
        ↓
Noise Removal (Patch Filtering)
        ↓
Raster → Polygon Conversion
        ↓
Management Zones
        ↓
Spray Priority Assignment
        ↓
Final Target Spraying Map
```

---

## 🛰️ Data Used

* **Satellite Source:** Sentinel-2 L2A
* **Bands Used:**
  * B04 → Red
  * B08 → Near Infrared (NIR)
* **Spatial Resolution:** 10 meters
* **Platform:** Microsoft Planetary Computer (STAC API)

---

## 🧮 Methodology

### 1. NDVI Calculation

[
NDVI = \frac{NIR - Red}{NIR + Red}
]

NDVI indicates vegetation health:

* High values → healthy vegetation
* Low values → weak or sparse vegetation

---

### 2. Vegetation Classification

| NDVI Range | Class               |
| ---------- | ------------------- |
| < 0.2      | Bare soil           |
| 0.2 – 0.4  | Weak vegetation     |
| 0.4 – 0.6  | Moderate vegetation |
| > 0.6      | Healthy vegetation  |

---

### 3. Weak Zone Detection

* Threshold: NDVI < 0.4
* Identifies low-vigor vegetation areas

---

### 4. Weed Suspicion Mapping

* Binary classification:

  * 1 → suspected zone
  * 0 → non-risk area

⚠️ Note: This represents **potential weed-prone zones**, not confirmed weed detection.

---

### 5. Noise Removal (Spatial Filtering)

* Connected component labeling
* Removal of small patches (< threshold pixels)
* Retains only meaningful spatial clusters

---

### 6. Raster to Polygon Conversion

* Converts raster patches into vector zones
* Enables real-world field interpretation

---

### 7. Management Zone Filtering

* Removes very small polygons
* Area-based filtering (m² threshold)

---

### 8. Spray Priority Assignment

| NDVI      | Priority |
| --------- | -------- |
| < 0.2     | High     |
| 0.2 – 0.4 | Medium   |
| > 0.4     | Low      |


## 📈 Key Insights

* NDVI effectively captures spatial variability in vegetation
* Weak zones highlight potential agronomic issues
* Spatial filtering improves decision reliability
* Polygon-based zones are suitable for real-world operations

---

## ⚠️ Limitations

* NDVI alone cannot confirm weed presence
* Low NDVI may also indicate:

  * nutrient deficiency
  * water stress
  * soil variability
  * pest damage

👉 This model provides **weed suspicion**, not definitive detection

---

## 🌱 Impact

* Supports precision agriculture practices
* Reduces unnecessary herbicide usage
* Promotes sustainable farming
* Enables data-driven crop management

---

## 🚀 Future Improvements

* Time-series NDVI analysis
* Integration with rainfall and soil data
* Machine learning-based classification
* Drone imagery integration
* Web GIS dashboard
* Cloud deployment (AWS + Docker pipelines)

---

## 💼 Use Case

This project is relevant for:

* Precision agriculture systems
* Digital farming platforms
* Crop monitoring solutions
* Agronomic decision support tools

---

## 👨‍💻 Author

**Gowtham Uppalapati**
Master’s Student — Sustainable International Agriculture
University of Göttingen
This project demonstrates how **remote sensing + geospatial analysis + data science** can be combined to create **practical agricultural decision-support systems**.
