# Mungana_RD
Some data science studies to assess the Cu mineralisation at Mungana and Red Dome (Chillagoe, NE QLD) with public GSQ data:
The goal is to identify the different types of Cu mineralisation particularly in ambiguous cases where high penalty elements may be offset by discrete "clean" Cu minerals (i.e., chalcopyrite). This kind of mineralisation might be hard to identify without machine learning, and here I present an example on how to apply machine learning to identify potentially valuable mineralised zones.

1. Here I present in file Cu_Fe_S.png the limitations of a standard Plotly 4D plot to assess the Cu mineralisation types "Cu vs Fe" with S and As represented by size and shade respectively. Nonetheless it can quickly illustrate the presence of Cu mineralisations with As well below the standards safety limit (2000 ppm) and high risk Cu mineralisations (oxide with high As) and ambiguous cases (high-grade Cu, S and As) that won't necessarily cluster together.

2. A PCA and PCA biplot (scikit-learn) is to be presented on the data points with Cu >= 1% (typical economic grade) to evaluate the control factor of high grade Cu / low As mineralisation. 

3. In the target dataset only the rows with Cu >=1 (or any other economically valuable grade) are chosen. This would avoid engineering additional rows with OneHotEncoder() or pandas.getdummies() that would introduce multicollinearity and overalap with the already present Cu_pct values. Removign Cu_pct values in favour of binaries such 0 = (Cu_pct <= 1)


The PCA Biplot integrantedd with sklearn K-Means shows th eformation fo 4 differnt clusters of Cu mienralisations:
Sulphide and Oxide mineralisations, that are subvided into As-poor and As-rich subtypes. 

The cluster of interest given (Fig. ) showing discrete sulphides is cluster 2, which contains high-As but extremely high-grade Cu in the sulphide form.
Other As-poor clusters are more self-explanatory and can be identified in other drill cores of the same deposit more easily by setting Cu, S, and As threshold values.
