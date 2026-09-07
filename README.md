# Mungana_RD

Geo-data science case study assessing Cu mineralisation at Mungana and Red Dome (Chillagoe, NE QLD) using public GSQ data.

The goal is to distinguish different types of Cu mineralisation, particularly ambiguous cases where high-penalty elements (e.g., As) coexist with discrete "clean" Cu minerals such as chalcopyrite (Figures 1 and 2). These cases are hard to identify by simple thresholding, so this project applies machine learning to flag potentially valuable mineralised zones. Data were collected with a Minalyzer™ at a 10 cm sampling interval on drill cores 845 and 883 (Mungana) and 187 and 997 (Red Dome).

<img width="981" height="1122" alt="JCU_29094_Lehrmann_2012_thesis" src="https://github.com/user-attachments/assets/cc563e35-4746-4c5e-86cd-38ac5bd5b0bd" />
<figcaption><i>Figure 1: Cu-bearing mineralisation at Mungana. The focus is on (c), which contains both pure chalcopyrite and tennantite (tn), a Cu sulpharsenide — evidence that clean chalcopyrite does occur in the Mungana deposit. From Lehrmann (2012).</i></figcaption>

<img width="1235" height="1412" alt="JCU_29094_Lehrmann_2012_thesis-RD_min_type" src="https://github.com/user-attachments/assets/bee9e508-5cde-4c30-95d9-66b42bed0bd1" />
<figcaption><i>Figure 2: Cu-bearing mineralisation at Red Dome. The focus is on (c) and (d), which contain pure chalcopyrite, discrete arsenopyrite (apy, an Fe sulpharsenide), and tennantite (tn, a Cu sulpharsenide) — evidence that clean chalcopyrite also occurs at Red Dome. From Lehrmann (2012).</i></figcaption>

## 1. Limitations of a standard 4D plot

A standard Plotly 4D plot ("Cu vs Fe", with S and As mapped to point size and shade) is used to assess Cu mineralisation types. While limited, it quickly highlights Cu mineralisation with As well below the safety threshold (2,000 ppm), high-risk oxide mineralisation with elevated As, and ambiguous cases (high-grade Cu, S, and As) that don't necessarily cluster together.

<img width="1520" height="809" alt="As_low" src="https://github.com/user-attachments/assets/20b7a0d0-89a6-4200-bca0-7bee709ba18f" />
<figcaption><i>Figure 3: Data points (10 cm interval scans) containing less than 2,000 ppm As.</i></figcaption>

<img width="1520" height="809" alt="As_high" src="https://github.com/user-attachments/assets/ab42100d-f899-4adb-b529-d15cb54eb3dd" />
<figcaption><i>Figure 4: Data points (10 cm interval scans) containing more than 2,000 ppm As, and therefore potentially unsafe to process.</i></figcaption>

## 2. PCA on the highest-grade drill core

The main focus is Red Dome drill core 997, which has the highest Cu grade. A PCA and PCA biplot (scikit-learn) were generated on data points with Cu ≥ 1% (a typical economic cutoff) to evaluate the type of Cu mineralisation present (Figure 5).

## 3. Feature selection and CoDA considerations

Only rows with Cu ≥ 1% (or another chosen economic threshold) are retained in the target dataset. This avoids engineering additional features via `OneHotEncoder()` or `pandas.get_dummies()`, which would introduce multicollinearity and overlap with the existing `Cu_pct` values. Replacing `Cu_pct` with a binarised encoding (0 for Cu_pct < 1%, 1 for Cu_pct ≥ 1%) would significantly distort the compositional data analysis (CoDA), particularly for data points where Cu is a major component (e.g., 20%).

<img width="1440" height="768" alt="RD_997_Mineralisation_types" src="https://github.com/user-attachments/assets/fb1b172e-c78c-456a-98aa-eb0c56f1dd93" />
<figcaption><i>Figure 5: PCA biplot of Cu mineralisation types in the Red Dome 997 drill core. Only data points with Cu ≥ 1% were selected. Arsenic content is colour-coded (yellow = high As).</i></figcaption>

## 4. Handling below-detection and not-detected values

Imputing below-detection and not-detected elements also raises issues. Using MICE or LrEM with an unadjusted mean MDL can produce chemically impossible data points — for example, a pure marble sample imputed with 2–5% Fe, which is not supported by imagery showing no Fe-associated hue.

## 5. Cluster of interest

The goal is not to identify self-explanatory mineralisation (low As, high Cu, either oxide or sulphide), but to identify and quantify the cluster containing discrete chalcopyrite (or another pure Cu-bearing sulphide) despite high arsenic grade.

Combining the PCA biplot with scikit-learn K-Means clustering identifies four clusters of Cu mineralisation: sulphide and oxide types, each split into As-poor and As-rich subtypes.

The cluster of interest (Figure 5) is Cluster 2, which shows high-As but extremely high-grade Cu in sulphide form — i.e., discrete, "clean" sulphide mineralisation despite elevated arsenic. The remaining, As-poor clusters are more self-explanatory and can be identified more easily in other drill cores from the same deposit by setting Cu, S, and As threshold values.
