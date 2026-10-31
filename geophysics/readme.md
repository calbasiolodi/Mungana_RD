# Magnetic and gravity PCA: full-area maps

## Overview

This analysis combines the magnetic TMI RGB image with the Red Dome gravity first vertical derivative (1VD) grayscale image over their shared survey footprint. Radiometry is excluded.

The gravity image contains eight horizontal and nine vertical cartographic grid lines. Grid-obscured pixels and a conservative margin were excluded before fitting the PCA. The model uses **183,964 observed shared pixels** and four variables: magnetic red, green and blue, plus one gravity grayscale channel. The gravity image's RGB channels are identical, so they are included once.

The first two PCs explain **81.05%** of the input image variance; the first three explain **91.35%**. PC3 has the strongest correlation with gravity grayscale (**+0.955541**). These are statistical relationships between rendered image channels, not evidence of particular geological causes.

This report covers the full-area maps and model fitted to the shared footprint.

![Full-area magnetic and gravity PCA component maps](figures/Mag_Gravity_all_PC_maps.png)

## Input data and spatial alignment

| Input | Source filename | Variables used |
|---|---|---|
| Magnetic TMI | `TMI_1357_Mag.tif` | Red, green and blue image channels |
| Gravity 1VD | `Gravimetry GSQ/Red Dome Gravity 1VD.tif` | One grayscale image channel |

- **Coordinate system:** GDA94 / MGA zone 55, EPSG:28355.
- **Analysis pixel size:** 21.360015 m, matching the native gravity grid.
- **Alignment:** magnetic RGB sampled by nearest neighbour onto the gravity grid.
- **Analysis area:** only pixels within both inferred valid survey footprints, with the gravity grid excluded.

The native gravity image has a fully opaque alpha channel. Its white background was inferred from grayscale value 254; enclosed white holes were retained, and 47 pixels belonging to tiny isolated edge ticks were removed. The magnetic image's edge-connected white background was excluded.

## Gravity grid removal

Long horizontal and vertical lines were detected through their image-wide darkening, and their approximately 2 km periodic spacing was checked. Detected rows and columns were expanded by one native pixel to cover antialiased edges.

| Pixel category within the shared footprint | Count | Use |
|---|---:|---|
| Observed, unmasked pixels | 183,964 | PCA fitting and observed score rasters |
| Grid-obscured pixels and conservative margin | 17,528 | Excluded from PCA; estimated only for display |
| Total shared display footprint | 201,492 | Observed pixels plus display estimates |

![Original gravity image, grid-removed display and grid exclusion mask](figures/Gravity_grid_removal_check.png)

Linear interpolation across the narrow grid bands creates a continuous **display copy only**. The original values hidden beneath printed grid lines cannot be recovered exactly from this image. Interpolated values do not contribute to model fitting, loadings or explained variance.

The [quality mask](data/Mag_Gravity_quality_mask.tif) records:

| Value | Meaning |
|---:|---|
| 0 | Outside the shared footprint |
| 1 | Observed pixel used for PCA |
| 2 | Excluded grid pixel; display estimate only |

## PCA method

The model uses scikit-learn PCA with all four components and the full singular value decomposition. Inputs are mean-centred, without standard-deviation scaling or whitening. This is covariance PCA: differences in channel variance influence component weighting.

For an input pixel `x`, the PC scores are:

```text
scores = (x - channel_means) @ coefficients
```

Rows of the coefficient matrix are input channels; columns are PCs.

| Input channel | Mean image value |
|---|---:|
| Magnetic red | 99.390756 |
| Magnetic green | 189.347470 |
| Magnetic blue | 127.430753 |
| Gravity 1VD grayscale | 177.780055 |

## Explained variance

| Component | Eigenvalue | Explained variance (%) | Cumulative (%) |
|---|---:|---:|---:|
| PC1 | 17710.886012 | 48.309246 | 48.309246 |
| PC2 | 12004.055925 | 32.742964 | 81.052210 |
| PC3 | 3776.792289 | 10.301799 | 91.354009 |
| PC4 | 3169.748539 | 8.645991 | 100.000000 |

![Scree plot showing individual and cumulative explained variance](figures/Mag_Gravity_scree.png)

[Download explained variance as CSV](data/Mag_Gravity_explained_variance.csv).

## Loadings

Three related quantities are supplied explicitly to avoid ambiguity about the term “loading.” Reversing the sign of an entire PC does not change its explained variance or relationships.

### Eigenvector coefficients

These are the weights used to calculate PC scores, corresponding to scikit-learn `components_.T`.

| Input channel | PC1 | PC2 | PC3 | PC4 |
|---|---:|---:|---:|---:|
| Magnetic red | +0.795016 | +0.372637 | +0.069949 | +0.473496 |
| Magnetic green | -0.207297 | -0.542511 | -0.158688 | +0.798453 |
| Magnetic blue | -0.558649 | +0.748355 | -0.041534 | +0.355179 |
| Gravity 1VD grayscale | -0.113529 | -0.082394 | +0.983972 | +0.110101 |

[Download coefficients as CSV](data/Mag_Gravity_coefficients.csv).

### Covariance loadings

Covariance loadings equal each eigenvector coefficient multiplied by the square root of its PC eigenvalue.

| Input channel | PC1 | PC2 | PC3 | PC4 |
|---|---:|---:|---:|---:|
| Magnetic red | +105.802529 | +40.827188 | +4.298756 | +26.658079 |
| Magnetic green | -27.587617 | -59.439181 | -9.752270 | +44.953323 |
| Magnetic blue | -74.346242 | +81.991992 | -2.552469 | +19.996742 |
| Gravity 1VD grayscale | -15.108629 | -9.027381 | +60.470581 | +6.198740 |

[Download covariance loadings as CSV](data/Mag_Gravity_loadings.csv).

### Channel–PC correlations

Correlation loadings equal covariance loadings divided by each input channel's sample standard deviation. They show the strength and direction of association between each image channel and each PC.

| Input channel | PC1 | PC2 | PC3 | PC4 |
|---|---:|---:|---:|---:|
| Magnetic red | +0.907577 | +0.350217 | +0.036875 | +0.228674 |
| Magnetic green | -0.344576 | -0.742410 | -0.121808 | +0.561478 |
| Magnetic blue | -0.660851 | +0.728812 | -0.022688 | +0.177748 |
| Gravity 1VD grayscale | -0.238743 | -0.142648 | +0.955541 | +0.097951 |

![Input-channel correlations with each principal component](figures/Mag_Gravity_loading_correlations.png)

[Download correlations as CSV](data/Mag_Gravity_correlations.csv).

## Full-area component maps

PNG maps use each PC's 2nd–98th percentile score limits. Values beyond those limits are clipped only for display. The map displays include PC scores calculated from interpolated gravity grid pixels for continuity; those positions are identified by quality-mask value 2.

Observed-score GeoTIFFs retain unscaled float32 scores, with **NoData = -9999** at obscured grid pixels and outside the shared footprint. The interpolated display products are supplied separately.

| Component | Full-area PNG map | Observed-score GeoTIFF |
|---|---|---|
| PC1 | [Map](figures/Mag_Gravity_PC1_map.png) | [GeoTIFF](data/Mag_Gravity_PC1.tif) |
| PC2 | [Map](figures/Mag_Gravity_PC2_map.png) | [GeoTIFF](data/Mag_Gravity_PC2.tif) |
| PC3 | [Map](figures/Mag_Gravity_PC3_map.png) | [GeoTIFF](data/Mag_Gravity_PC3.tif) |
| PC4 | [Map](figures/Mag_Gravity_PC4_map.png) | [GeoTIFF](data/Mag_Gravity_PC4.tif) |

## Data products

| File | Contents |
|---|---|
| [Observed PC scores](data/Mag_Gravity_PCA_observed_all.tif) | All four PC bands; grid pixels excluded |
| [PC display estimates](data/Mag_Gravity_PCA_display_estimates_all.tif) | All four PC bands including interpolated grid estimates, for display only |
| [Gravity analysis image](data/Gravity_1VD_grid_removed_analysis.tif) | Unmodified observed grayscale values; grid and background set to NoData |
| [Gravity display image](data/Gravity_1VD_grid_removed_display.tif) | Repaired RGBA image with interpolated grid bands |
| [Grid exclusion mask](data/Gravity_grid_exclusion_mask.tif) | Detected grid and conservative margin |
| [PCA quality mask](data/Mag_Gravity_quality_mask.tif) | Observed, estimated-display and outside-footprint categories |
| [Fitted model](data/Mag_Gravity_model.npz) | Channel means, coefficients, eigenvalues and explained variance ratios |
| [Full-area diagnostics](data/Mag_Gravity_full_area_diagnostics.json) | Model, alignment, grid detection and validation metadata |

## Validation and interpretation limits

Validation checked the independently calculated covariance eigenvalues, PC orthogonality, diagonal score covariance, inverse reconstruction, saved individual scores and masks. All retained observed gravity values are unchanged. Maximum inverse reconstruction error from the four float32 PCs was **0.000010114 image units**.

The inputs are rendered images. Magnetic RGB values are map colours, and gravity grayscale is an image encoding of a 1VD map. These results describe image variation; they do not recover magnetic or gravity measurements in physical units. White-background detection and interpolated grid displays are assumptions made from the available images. Geological interpretation requires comparison with original geophysical data and independent geological evidence.

Recorded software versions: rasterio 1.5.2, scikit-learn 1.9.0 and NumPy 2.4.6.

## Using this report on GitHub

Edit this `README.md` as ordinary Markdown. Upload it together with the accompanying `figures/` and `data/` folders, retaining their relative locations. All image and download links use repository-relative paths; no external image hosting is required.


