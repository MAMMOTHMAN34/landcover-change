# Land Cover Change Detection: Riau, Sumatra

Deep-learning computer vision on real satellite imagery to map and quantify
deforestation, then tie forest loss to palm-oil economics.

---

## Why this project

The lowland forests of Riau, Sumatra have been among the fastest-disappearing
on Earth, cleared largely for oil-palm plantations. This project asks two
questions with open data:

1. **Can a segmentation model trained on raw Sentinel-2 imagery map land cover
   accurately enough to track change over time?**
2. **Does the palm-oil commodity price help explain the *rate* of forest loss,
   and is there a lag?**

It combines satellite remote sensing, deep-learning computer vision, and a bit
of environmental economics.

## What it does

- Pulls **cloud-masked Sentinel-2** surface-reflectance composites (free, ESA
  Copernicus via Google Earth Engine) for a Riau deforestation front, one per
  year for **2019 / 2021 / 2024**.
- Trains a **U-Net** to segment 5 land-cover classes: forest, agriculture,
  urban, water, and bare, using **ESA WorldCover (10m)** as the label source.
- Runs inference across all three years and **quantifies per-class change**.
- Cross-checks forest loss against **Hansen Global Forest Change** (annual,
  2001–2023) and runs a **lagged regression** vs **World Bank palm-oil prices**.
- Outputs before/after maps, a forest-cover time series, and the economic
  correlation plot.

## Key design decisions

- **Labels from a published product.** Hand-labelling satellite pixels is
  not feasible, so the U-Net is trained to reproduce ESA WorldCover from raw S2
  bands, which is a legitimate segmentation task.
- **Composites, not single scenes.** Riau is extremely cloudy, thus should median-
  composite cloud-masked imagery over the dry season (Jun–Sep) each year.
- **Two evidence streams for the economics.** The U-Net gives 3 high-detail
  snapshots (the CV showcase); Hansen GFC gives ~23 annual points so the
  price→forest-loss regression is actually meaningful.
- **"Forest" means tree cover, and the data is imbalanced on purpose.** Every
  Riau AOI reads as 85-93% forest because WorldCover labels mature oil palm as
  Tree cover. Rather than chase a balanced box that doesn't exist, I keep the
  most class-diverse AOI (Indragiri coast), handle the imbalance with a weighted
  loss + per-class IoU, and measure deforestation as tree-cover *loss* over
  time. Splitting natural forest from plantation (via a dedicated oil-palm map)
  is the planned extension, not the baseline.

## Stack

Python · Google Earth Engine · PyTorch (`segmentation-models-pytorch`) ·
rasterio / GeoPandas · statsmodels · Colab (GPU training)

## Project structure

```
landcover-change/
├── configs/            # study area, years, class scheme, GEE collection ids
├── src/landcover/      # reusable modules (data, model, analysis)
├── notebooks/          # exploration + Colab training notebooks
├── data/               # raw / processed / tiles  (gitignored)
└── outputs/            # figures + maps  (gitignored)
```

## Setup

See [`docs/setup.md`](docs/setup.md) for Google Earth Engine registration and
local environment setup.
