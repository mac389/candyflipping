import pandas as pd
import numpy as np 

from pprint import pprint 

list_of_drugs = open('./drugs').read().splitlines()
correlation = np.loadtxt('./comention-matrix.csv',delimiter=',',dtype=float)
correlation /= 100

CUTOFF_CORRELATION = 0.72
#Corresponds to 85th percentile 

combinations = [(list_of_drugs[i],list_of_drugs[j]) 
					for i,j in zip(*np.where(correlation>CUTOFF_CORRELATION))]

with open('./significant-combinations','wb') as fout:
	for combination in combinations:
		print>>fout,'_'.join(combination)