# Sample Tomato Images

The demo sample set is stored in:

```text
sample_data/images/tomato_web/
```

The set is built from Wikimedia Commons images with license metadata recorded in:

```text
sample_data/images/tomato_web/ATTRIBUTION.md
sample_data/images/tomato_web/manifest.json
```

Some difficult demo cases, such as blurry photos, dark photos, poor angles, and dry-looking/water-stress-like photos, are locally derived from licensed Wikimedia Commons source images. They are marked as derived in the manifest and should be described as demo/evaluation samples rather than real diagnostic labels.

To refresh the images:

```bash
python scripts/download_tomato_samples.py
```

Target coverage:

| # | Condition | Local sample |
|---|---|---|
| 1 | Tomato whole plant | `01_tomato_whole_plant.jpg` |
| 2 | Leaf close-up | `02_tomato_leaf_closeup.jpg` |
| 3 | Soil condition | `03_tomato_soil_condition.jpg` |
| 4 | Weeds/context visible | `04_tomato_weeds_context.jpg` |
| 5 | Fruiting | `05_tomato_fruiting.jpg` |
| 6 | Water-stress-like | `06_tomato_water_stress_like_derived.jpg` |
| 7 | Looks healthy/normal | `07_tomato_healthy.jpg` |
| 8 | Blurry photo | `08_tomato_blurry_derived.jpg` |
| 9 | Night/dark photo | `09_tomato_dark_derived.jpg` |
| 10 | Poor angle | `10_tomato_bad_angle_derived.jpg` |
