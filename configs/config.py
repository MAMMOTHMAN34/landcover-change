"""Central configuration for the land-cover-change project.

Everything that another module might need to agree on (the study area, the
years we compare, the class scheme, the GEE collection ids) lives here so we
only define it once.
"""

# --------------------------------------------------------------------------
# Area of interest — Riau province, Sumatra
# --------------------------------------------------------------------------
# A ~55 x 55 km box over the Kampar/Pelalawan lowlands, one of the most
# intense palm-oil deforestation fronts in Indonesia. Format: [W, S, E, N]
# (lon/lat, EPSG:4326). Tune these bounds once we eyeball the first composite.
AOI_BBOX = [101.5, 0.0, 102.0, 0.5]
AOI_NAME = "riau_kampar"

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
# Land-cover class scheme (5 classes)
# --------------------------------------------------------------------------
# Trained against ESA WorldCover (10m) as the label source, remapped from its
# native classes into our coarser 5-class scheme.
CLASSES = {
    0: "forest",
    1: "agriculture",   # incl. oil-palm plantation / cropland
    2: "urban",         # built-up
    3: "water",
    4: "bare",          # bare / sparse ground
}
N_CLASSES = len(CLASSES)

# Display colours (hex) for maps, indexed by class id above.
CLASS_COLORS = ["#1b7837", "#e6c200", "#d7191c", "#2c7fb8", "#bdbdbd"]

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
HANSEN_GFC = "UMD/hansen/global_forest_change_2023_v1_11"  # annual forest loss
