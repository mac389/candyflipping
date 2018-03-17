import networkx as nx 
import pandas as pd 
import matplotlib.pyplot as plt 

from networkx.drawing.nx_agraph import graphviz_layout

df = pd.read_csv('./flat_correlation.csv')

G = nx.from_pandas_dataframe(df,'Drug 1','Drug 2','Correlation')
#nx.write_gexf(G,'./flat_correlation.gexf')

weights = [G[u][v]['Correlation']*2 for u,v in G.edges()]

nx.draw(G, pos=graphviz_layout(G, prog='neato'), with_labels=True, node_color='w', 
				font_size=14, width=weights)
plt.show()