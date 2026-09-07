# Mungana_RD
Some data science specific case studies to assess the Cu mineralisation at Mungana and Red Dome (Chillagoe, NE QLD) with public GSQ data:
The goal is to identify the different types of Cu mineralisation particularly in ambiguous cases where high penalty elements may be offset by discrete "clean" Cu minerals (i.e., chalcopyrite). This kind of mineralisation might be hard to identify without machine learning, and here I present an example on how to apply machine learning to identify potentially valuable mineralised zones. The data were collected with Minalyzer(TM) and the chosen interval for this particular study is 10 cm, on drill cores 845, 883 (Mungana) and 187 and 997 Red Dome.

1. Here I present in  the limitations of a standard Plotly 4D plot to assess the Cu mineralisation types "Cu vs Fe" with S and As represented by size and shade respectively. Nonetheless it can quickly illustrate the presence of Cu mineralisations with As well below the standards safety limit (2000 ppm) and high risk Cu mineralisations (oxide with high As) and ambiguous cases (high-grade Cu, S and As) that won't necessarily cluster together.


<img width="1520" height="809" alt="As_low" src="https://github.com/user-attachments/assets/20b7a0d0-89a6-4200-bca0-7bee709ba18f" />
<figcaption><i>Figure 1: Datapoints (10 cm interval scan) containing less than 2000 ppm in As.</i></figcaption>
<img width="1520" height="809" alt="As_high" src="https://github.com/user-attachments/assets/ab42100d-f899-4adb-b529-d15cb54eb3dd" />
<figcaption><i>Figure 2: Datapoints (10 cm interval scan) containing more than 2000 ppm in As, thus might be unsafe to process.</i></figcaption>

2. The main focus is drill core Red Dome 997, since it has the highest grade of Cu. Thus, A PCA and PCA biplot (scikit-learn) is to be presented on the data points with Cu >= 1% (typical economic grade) to evaluate the type of Cu mineralisation (Figure 3).



<img width="981" height="1122" alt="JCU_29094_Lehrmann_2012_thesis" src="https://github.com/user-attachments/assets/cc563e35-4746-4c5e-86cd-38ac5bd5b0bd" />
<figcaption><i>Figure 3: the Cu-bearing mineralisation in Mungana, the focus in on c), that contains both pure chalcopyrite and tennantite (tn) whihc is a Cu sulpharsenide. Thus providing evidence that clean chalcopyrite can be actually found in Mungana deposit. From Lehrmann (2012)</i></figcaption>

<img width="1235" height="1412" alt="JCU_29094_Lehrmann_2012_thesis-RD_min_type" src="https://github.com/user-attachments/assets/bee9e508-5cde-4c30-95d9-66b42bed0bd1" />
<figcaption><i>Figure 3: the Cu-bearing mineralisation in Red Dome, the focus in on c) and d). This mineralisaiton contains both pure chalcopyrite, discrete arsenopyrite (apy) that is Fe sulpharsenide, tennantite (tn) which is a Cu sulpharsenide. Thus providing evidence that clean chalcopyrite can be actually found in Mungana deposit. From Lehrmann (2012)</i></figcaption>

3. In the target dataset only the rows with Cu >=1 (or any other economically valuable grade) are chosen. This would avoid engineering additional rows with OneHotEncoder() or pandas.getdummies() that would introduce multicollinearity and overalap with the already present Cu_pct values. Removing Cu_pct values in favour of binarised dummies/encoders such as: 0 = (["Cu_pct"] <= 1) & 1 = (["Cu_pct"] >= 1), would distort CoDA significantly paritcualrly in datapoints where Cu is a main componens (e.g., 20%).

<img width="1440" height="768" alt="RD_997_Mineralisation_types" src="https://github.com/user-attachments/assets/fb1b172e-c78c-456a-98aa-eb0c56f1dd93" />
<figcaption><i>Figure 5: a PCA biplot wiht the different types of Cu mineralisations in Red Dome 997 drill core. Only datapoints with Cu >= 1% were selected. Arsenic content is color coded (yellow = high As)</i></figcaption>

4. There are also significant issues to raise with imputting below detection and not detected elements. Using MICE or LrEM by inserting the mean MDL without any tweak would introduce chemically impossible datapoints, whenthe MDL for a specific datapoint is missing, such as the instance of pure marble containing Fe contents in the order of miner (2 to 5%) that is not supported by imagery (no hue indicating Fe mineralisation).

5. The goal is not identify self-explanatory mienralisations (low As, High Cu, either ox. or sulph.), rather it is to identify and quantify the cluster that might contian discrete chalcopyrite (or any other pure Cu-bearing sulphide) despite high grade arsenic.

The PCA Biplot integrantedd with sklearn K-Means shows th eformation fo 4 differnt clusters of Cu mienralisations:
Sulphide and Oxide mineralisations, that are subvided into As-poor and As-rich subtypes. 

The cluster of interest given (Fig. ) showing discrete sulphides is cluster 2, which contains high-As but extremely high-grade Cu in the sulphide form.
Other As-poor clusters are more self-explanatory and can be identified in other drill cores of the same deposit more easily by setting Cu, S, and As threshold values.
