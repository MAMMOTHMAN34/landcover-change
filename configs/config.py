"""Central configuration for the land-cover-change project.

Everything that another module might need to agree on (the study area, the
years we compare, the class scheme, the GEE collection ids) lives here so we
only define it once.
"""

# --------------------------------------------------------------------------
# Area of interest: Riau province, Sumatra
# --------------------------------------------------------------------------
# A ~0.5deg box over the Indragiri Hilir coast (SE Riau): a smallholder
# oil-palm / coconut / cropland mosaic with intact peat forest inland and a
# real coastal water class. Chosen from notebook 03 as the most class-diverse
# of the candidates tested (~85% forest / 10% agriculture / 4% water).
# Format: [W, S, E, N] in lon/lat (EPSG:4326).
#
# NB: every Riau box reads as 85-93% "forest" because WorldCover maps mature
# oil palm as Tree cover. We can't fix the imbalance by moving the box, so we
# handle it in the model (weighted loss + per-class IoU) and frame the change
# signal as tree-cover *loss* over time. Separating forest vs plantation (via a
# dedicated oil-palm layer) is the planned extension, not the baseline.
AOI_BBOX = [102.9, -0.6, 103.4, -0.1]
AOI_NAME = "indragiri_coast"

# --------------------------------------------------------------------------
# Time snapshots for the U-Net change-detection story
# --------------------------------------------------------------------------
# We build one cloud-masked composite per year over the dry-season window
# (drier, fewer clouds in central Sumatra ~ Jun–Sep).
# NB: starts at 2019, not 2017 — Sentinel-2 L2A surface reflectance only has
# systematic coverage over Indonesia from ~2019 (2017 returns 0 scenes).
SNAPSHOT_YEARS = [2019, 2021, 2024]
DRY_SEASON = ("06-01", "09-30")   # (month-day start, month-day end)

# --------------------------------------------------------------------------
# Land-cover class scheme (4 classes)
# --------------------------------------------------------------------------
# Trained against ESA WorldCover (10m) as the label source, remapped from its
# native classes into our coarser scheme.
#
# Originally 5 classes, but 'bare' came back as ~0.02% of the Indragiri-coast
# AOI — a degenerate class that broke loss weighting and that the model can't
# learn from. We fold bare / sparse ground into 'agriculture' (open non-forest
# ground). WorldCover native 60/70/100 therefore map to class 1; existing tiles
# (which still carry a stray class 4) are remapped 4 -> 1 in the data loader.
CLASSES = {
    0: "forest",
    1: "agriculture",   # incl. oil-palm plantation / cropland / bare ground
    2: "urban",         # built-up
    3: "water",
}
N_CLASSES = len(CLASSES)

# Display colours (hex) for maps, indexed by class id above.
CLASS_COLORS = ["#1b7837", "#e6c200", "#d7191c", "#2c7fb8"]

# --------------------------------------------------------------------------
# Sentinel-2 settings
# --------------------------------------------------------------------------
S2_COLLECTION = "COPERNICUS/S2_SR_HARMONIZED"   # surface reflectance, harmonized
S2_CLOUD_PROB = "COPERNICUS/S2_CLOUD_PROBABILITY"
CLOUD_PROB_THRESHOLD = 40        # mask pixels with cloud prob above this %
# Bands we export (10m + 20m optical). B8 = NIR, B11/B12 = SWIR — key for veg.
S2_BANDS = ["B2", "B3", "B4", "B8", "B11", "B12"]
EXPORT_SCALE = 10                # metres per pixel

# --------------------------------------------------------------------------
# Label / reference products
# --------------------------------------------------------------------------
WORLDCOVER = "ESA/WorldCover/v200"           # 2021 land cover, training labels
HANSEN_GFC = "UMD/hansen/global_forest_change_2025_v1_13"  # annual forest loss (to 2024)
