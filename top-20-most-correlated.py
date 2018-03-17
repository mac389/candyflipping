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


flat_correlation = correlation.stack().reset_index()
flat_correlation.columns = ['Drug 1','Drug 2','Correlation']
flat_correlation = flat_correlation[(flat_correlation['Correlation']!=-2) & (flat_correlation['Correlation'].abs()>0.72) & (flat_correlation['Correlation']!=1)]
flat_correlation.to_csv('./flat_correlation.csv')

flat_correlation = flat_correlation[(flat_correlation['Correlation']>cutoff_correlation) & (flat_correlation['Correlation']!=1)]
tiny_correlation = flat_correlation.pivot(index='Drug 1',columns='Drug 2', values='Correlation').fillna(-2)
g = sns.clustermap(tiny_correlation, mask= tiny_correlation == -2,vmin=-1,vmax=1, cmap='seismic',figsize=(12,12))
plt.setp(g.ax_heatmap.yaxis.get_majorticklabels(), rotation=0)
plt.setp(g.ax_heatmap.xaxis.get_majorticklabels(), rotation=90)
g.savefig('./tiny-comention-matrix.png')
