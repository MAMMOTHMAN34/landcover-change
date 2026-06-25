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
- Trains a **U-Net** to segment 4 land-cover classes: forest, agriculture,
  urban, and water, using **ESA WorldCover (10m)** as the label source. (A 5th
  class, bare ground, was dropped as it's ~0.02% of this coastal AOI.)
- Runs inference across all three years and **quantifies per-class change**.
- Cross-checks forest loss against **Hansen Global Forest Change** (annual,
  2001–2023) and runs a **lagged regression** vs **World Bank palm-oil prices**.
- Outputs before/after maps, a forest-cover time series, and the economic
  correlation plot.

## Key design decisions

- **Labels from a published product.** Hand-labelling satellite pixels is
  not feasible, so the U-Net is trained to reproduce ESA WorldCover from raw S2
  bands.
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

## Results & findings

**Segmentation (U-Net, 4-class, validation):** best **mIoU 0.716**.

| class | IoU | note |
|---|---|---|
| water | 0.93 | spectrally distinct, easiest |
| forest | 0.86 | abundant, well-learned |
| urban | 0.58 | only 0.6% of pixels — class weighting earns this |
| agriculture | 0.41 | the hard catch-all; shares a fuzzy edge with "forest" |

**Change detection (2019 → 2024) — and an honest caveat.** Run across the three
years, the model reports forest *increasing* (net **+110 km²**; share 83.5% →
87.1%), which looks backwards for a deforestation front. It isn't reforestation —
it's two effects worth understanding:

1. **Plantation maturation reads as "forest gain."** Mature oil palm is labelled
   Tree cover, so clear→replant→regrow nets out as a *gain* in tree cover even as
   natural forest is lost.
2. **Year-to-year noise.** The trend is non-monotonic (83.5 → 82.1 → 87.1) — the
   fingerprint of composite/model inconsistency, not a real trajectory.

**Takeaway:** the U-Net is strong for **land-cover mapping**, but a 3-snapshot
model difference is *not* a reliable net-deforestation metric here. That is
exactly why the deforestation statistics come from **Hansen** (annual, 2001–2023,
which flags loss *events*) rather than from differencing model snapshots.

<!-- TODO: add Step 6 economic result — palm-oil price vs Hansen forest loss, lag, correlation -->

## Stack

Python ; Google Earth Engine ; PyTorch (`segmentation-models-pytorch`) ;
rasterio / GeoPandas ; statsmodels ; Colab (GPU training)

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
