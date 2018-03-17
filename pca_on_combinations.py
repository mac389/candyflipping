import pandas as pd
import numpy as np 

import matplotlib.pyplot as plt 
from sklearn.decomposition import PCA as sklearnPCA

pca = sklearnPCA(n_components=3)

list_of_drugs = open('./drugs','rb').read().splitlines()
df = pd.read_csv('./comention-matrix.csv',header=None)
df.index = list_of_drugs
df.columns = list_of_drugs

x  = df.corr().fillna(0)

x_transformed = pca.fit_transform(x)

print x_transformed.shape


#Y_sklearn = sklearn_pca.fit_transform(X_std)



fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(x_transformed[:,2],x_transformed[:,0],'.')
plt.show()