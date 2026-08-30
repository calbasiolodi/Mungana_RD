import pandas as pd
import matplotlib.pyplot as plt
import mpl_axes_aligner
from sklearn.decomposition import PCA

source_path: str = r"C:\Users...\RD_997_clr_transformed_only_elements.csv"

df = pd.read_csv(source_path)

df_cp = df.copy()

df_cp.drop(columns=['Tray_name','From_m', 'To_m'], inplace=True)

X = df_cp.iloc[:, :-1].values          
feature_names = df_cp.columns[:-1]    

# 1. Fit PCA
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X)

PCA_components = pca.components_
components_df = pd.DataFrame(PCA_components, columns=feature_names, index=['PC1', 'PC2'])

# 2. Prepare Scores DataFrame with 'As'
dfScores = pd.DataFrame(X_pca, columns=['PC1', 'PC2'])
dfScores['As_ppm'] = df_cp['As_ppm'].values

# 3. Biplot function
def biplot(dfScores: pd.DataFrame, dfLoadings: pd.DataFrame, exp_var: list = None) -> None:
    fig, ax = plt.subplots(figsize=(15, 8))
    # Color code by As
    scatter = ax.scatter(
        dfScores.PC1.values, 
        dfScores.PC2.values, 
        c=dfScores['As_ppm'], 
        cmap='viridis',
        alpha=0.8,
        edgecolors='k',
        linewidth=0.3
    )
    
    # Add colorbar
    cbar = fig.colorbar(scatter, ax=ax, pad=0.08)
    cbar.set_label('As Content', fontsize=11, weight='bold')

    if exp_var is not None:
        ax.set_xlabel(f"PC1 ({exp_var[0] * 100:.2f}%)", fontsize=10)
        ax.set_ylabel(f"PC2 ({exp_var[1] * 100:.2f}%)", fontsize=10)
    else:
        ax.set_xlabel("PC1", fontsize=10)
        ax.set_ylabel("PC2", fontsize=10)

    ax2 = ax.twinx().twiny()
    font = {'color': 'red', 'weight': 'bold', 'size': 11}

    for col in dfLoadings.columns.values:
        tipx = dfLoadings.loc['PC1', col]
        tipy = dfLoadings.loc['PC2', col]
        ax2.arrow(0, 0, tipx, tipy, color='red', alpha=0.5)
        ax2.text(tipx * 1.05, tipy * 1.05, col, fontdict=font, ha='center', va='center')

    mpl_axes_aligner.align.xaxes(ax, 0, ax2, 0, 0.5)
    mpl_axes_aligner.align.yaxes(ax, 0, ax2, 0, 0.5)

# 4. Plot
biplot(dfScores, components_df, exp_var=pca.explained_variance_ratio_)
plt.savefig(r"C:\Users\cesar\Documents\Mineral deposits PyTorch and Python\Mungana RD_report\RD 997 From scratch\custom\PCA_BP_cc_Si.png")
plt.show()

