# Mungana_&_RD

Geo-data science case study assessing Cu mineralisation at Mungana and Red Dome (Chillagoe, NE QLD) using public GSQ data.

The goal is to distinguish different types of Cu mineralisation, particularly ambiguous cases where high bulk-rock content of penalty elements (e.g., As in this particular study) coexist with discrete "clean" Cu minerals such as chalcopyrite (Figures 1 and 2). These cases are hard to identify by simple thresholding, i.e. setting boolean rules such as clean_Cu__mineralisation = [Cu_pct >= 1] & [As_ppm < 2000] as there is significant variability among measurements.  So this project applies simple and auditable machine learning (Scikit-learn PCA and XGBoost in_dev) to flag potentially valuable high-grade Cu mineralised zones despite unusually high-arsenic. Data were collected with a Minalyzer™ at a 10 cm sampling interval on drill cores 845 and 883 (Mungana) and 187 and 997 (Red Dome).
<img width="3210" height="3684" alt="chapter-12-mungana-red-dome_deposits_NEQ" src="https://github.com/user-attachments/assets/05ed30ff-8127-44fa-96c3-b6c89f20106a" />
<figcaption><i>A map showing Mungana and Red Dome in the context of NE QLD. From GSQ report.</i></figcaption>
<img width="981" height="1122" alt="JCU_29094_Lehrmann_2012_thesis" src="https://github.com/user-attachments/assets/cc563e35-4746-4c5e-86cd-38ac5bd5b0bd" />
<figcaption><i>Figure 1: Cu-bearing mineralisation at Mungana. The focus is on (c), which contains both pure chalcopyrite and tennantite (tn), a Cu sulpharsenide evidencing that clean chalcopyrite does occur in the Mungana deposit. From Lehrmann (2012).</i></figcaption>

<img width="1235" height="1412" alt="JCU_29094_Lehrmann_2012_thesis-RD_min_type" src="https://github.com/user-attachments/assets/bee9e508-5cde-4c30-95d9-66b42bed0bd1" />
<figcaption><i>Figure 2: Cu-bearing mineralisation at Red Dome. The focus is on (c) and (d), which contain pure chalcopyrite, discrete arsenopyrite (apy, an Fe sulpharsenide), and tennantite (tn, a Cu sulpharsenide) indicating that clean chalcopyrite also occurs at Red Dome. From Lehrmann (2012).</i></figcaption>

## 1. Limitations of a standard 4D plot

A standard Plotly 4D plot ("Cu vs Fe", with S and As coded to datapoint size and shade respectiviely) is used to assess Cu mineralisation types. While limited, it quickly highlights Cu mineralisation, display As when below the safety threshold (2,000 ppm), the pyrite tie-line from Escolme et al. (2017), high-risk to process oxide mineralisation with elevated As, and ambiguous cases (high-grade Cu, S, and As) that do not necessarily cluster together.

<img width="1520" height="809" alt="As_low" src="https://github.com/user-attachments/assets/20b7a0d0-89a6-4200-bca0-7bee709ba18f" />
<figcaption><i>Figure 3: Data points (10 cm interval scans) containing less than 2,000 ppm As. </i></figcaption>

<img width="1520" height="809" alt="As_high" src="https://github.com/user-attachments/assets/ab42100d-f899-4adb-b529-d15cb54eb3dd" />
<figcaption><i>Figure 4: Data points (10 cm interval scans) containing more than 2,000 ppm As, and therefore potentially unsafe to process. Dashed line = Pyrite tie-line.</i></figcaption>

## 2. PCA on the highest-grade Cu-bearing drill core

The main focus is Red Dome drill core 997, which has the highest Cu grade among the other 3 drill core from the deposit (RD187, Mungana_845, Mungana_883). A PCA and PCA biplot (scikit-learn) were generated on data points with Cu ≥ 1% (a typical economic cutoff) to evaluate the type of Cu mineralisation present (Figure 5).

## 3. Feature selection and CoDA considerations

Only rows with Cu ≥ 1% (or another chosen economic threshold) are retained in the target dataset. This avoids engineering additional features via `OneHotEncoder()` or `pandas.get_dummies()`, (i.e., a category column saying Cu>=1 equals 0 or 1) which would introduce multicollinearity, and overlap with the existing `Cu_pct` values label. Hence, replacing `Cu_pct` with a binarised encoding (0 for Cu_pct < 1%, 1 for Cu_pct ≥ 1%) would significantly distort the compositional data analysis (CoDA), particularly for data points where Cu is a major component (e.g., 20%). Data were subsequently scaled with CLR (from scikit-bio) which is the standard pipeline with CoDA.

<img width="1440" height="768" alt="RD_187_mineralisations" src="https://github.com/user-attachments/assets/1612a8d0-e846-40f7-ad2a-574987eacdf1" />

<figcaption><i>Figure 5: PCA biplot of Cu mineralisation types in the Red Dome 997 drill core. Only data points with Cu ≥ 1% were selected. Arsenic content is colour-coded (yellow = high As). The oxides are associated with silica-bearing lithology (possibly garnets and micas, with less important calc-silicate component), while sulphides are associated with Ca-bearing lithologies (most likely marble and to a minor extent calc-silicates) </i></figcaption>

## 4. Handling below-detection and not-detected values

Imputing below-detection and not-detected elements also raises issues if performed without checking carefully. Using MICE or LrEM with a mean MDL from the entire drillcore can produce chemically impossible data points. For instance, a pure marble sample with ND Fe might be imputted with 2–5% Fe (the mean LOD of all XRF measurements in the overall drill core), which is not supported by imagery showing no Fe-associated hue.
It may be a better option instead to cap a certain threshold the maximum value inserted by the imputter when in a specific row the respective MDL is absent.

Another alternative explored sideways, but not in this published project would be using a bootstrap method for ND and BDL elements capped at an arbitrarily low percentage such as 0.05 % when the element is in percent or 0.1 when the element is in ppm. These small numbers would not distort significantly the compositional data that would be then be recalculated, and it is still a more geochemically acceptable practice to assume a very small value when the instrument did not detect a specific element.

## 5. Cluster of interest

The goal is not to identify self-explanatory mineralisations types (low As, high Cu, either oxide or sulphide) that can be selected with simple boolean rules (e.g., ["As_ppm"] < 2000), but to identify and quantify the sulphide-bearing cluster cluster containing discrete chalcopyrite (or another pure Cu-bearing sulphide) despite high arsenic grade, and whether it is linked to specific lithologies.

Combining the PCA biplot with clustering (K-means will be added) identifies four clusters of Cu mineralisation: sulphide and oxide types, each split into As-poor and As-rich subtypes.

The cluster of interest (Figure 5) is Cluster 2, which shows high-As but extremely high-grade Cu in sulphide form — i.e., discrete, "clean" sulphide mineralisation despite elevated arsenic. The remaining, As-poor clusters are more self-explanatory and can be identified more easily in other drill cores from the same deposit by setting Cu, S, and As threshold values.

A robust PCA did not yield significantly different results.

## 6. IN DEV: SHAP and XGBoost on drillcores of the same deposit with training data from RD 187 drillcore
