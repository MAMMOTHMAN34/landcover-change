# Setup

## 1. Google Earth Engine access (free)

GEE is free for research/non-commercial use, but needs a one-time signup tied
to a Google Cloud project.

1. **Register:** go to <https://earthengine.google.com/> and click *Get
   Started* / sign in with your Google account.
2. **Create / pick a Cloud project.** When prompted, choose *Register a
   project for non-commercial / research use* and create a new Cloud project
   (e.g. `landcover-riau`). Note the **project id** — we'll need it to
   authenticate. No billing or credit card is required for the free tier.
3. **Wait for activation.** Approval is usually instant-to-a-few-minutes.

That's all you need for now. We authenticate from code in Step 2.

> Keep the project id handy — paste it back to me and we'll wire it into the
> auth call. **Never commit credential JSON files** (`.gitignore` already
> blocks them).

## 2. Local Python environment

Used for data wrangling, analysis, and figures. (U-Net *training* runs on
Colab, not locally.)

```bash
cd landcover-change
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

> **Note on GDAL/rasterio:** these can be fiddly to pip-install on macOS. If
> `pip install rasterio` fails, the easiest fix is conda:
> `conda install -c conda-forge gdal rasterio geopandas`. We'll sort this in
> Step 2 only if it actually bites — the GEE-side work doesn't need it.

## 3. Authenticate Earth Engine (Step 2, later)

Once registered, a one-time browser auth:

```python
import ee
ee.Authenticate()                       # opens a browser, paste the token back
ee.Initialize(project="YOUR_PROJECT_ID")
```
