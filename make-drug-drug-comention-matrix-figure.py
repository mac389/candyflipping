import matplotlib.pyplot as plt 
import numpy as np 
import pandas as pd 
import seaborn as sns 

comention_matrix = np.loadtxt('./comention-matrix.csv', delimiter=',')
drugs = open('./drugs','rb').read().splitlines()

df = pd.DataFrame(data=comention_matrix,index=drugs,columns=drugs)

correlation = df.corr().fillna(-2)
cutoff_percentile = 85
#0.72

cutoff_correlation = np.percentile(np.absolute(correlation),cutoff_percentile)
print cutoff_correlation
g = sns.clustermap(correlation, mask= correlation == -2,vmin=-1,vmax=1, cmap='seismic',figsize=(12,12))
plt.setp(g.ax_heatmap.yaxis.get_majorticklabels(), rotation=0)
plt.setp(g.ax_heatmap.xaxis.get_majorticklabels(), rotation=90)
g.savefig('./comention-matrix.png')