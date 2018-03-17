import itertools

import numpy as np 
import seaborn as sns

from pymongo import MongoClient
from tqdm import tqdm
from pprint import pprint 

client = MongoClient()
db = client['candyflipping']
combinations = db['text_by_drug_combinations']

#What is the distribution of p-values?

p_value_distribution = combinations.find({"analysis":{"$exists":"true"}},
							{"analysis.test.p-value":1,"drugs":1,"_id":0})
drug_combinations, p_value_distribution = zip(*[(item["drugs"],item["analysis"]["test"]["p-value"])
							for item in p_value_distribution])

BONFERRONI_CORRECTION_FACTOR = 624
#Could use Benjamini-Hochberg, but Bonferroni is better known
p_value_distribution = np.array(p_value_distribution)

significant_combinations =  np.array(drug_combinations, dtype='str')[p_value_distribution<(0.01/BONFERRONI_CORRECTION_FACTOR)]
print len(significant_combinations)

with open('basis-map.csv','wb') as fout:
	print>>fout,'source,target,weight'
	for combination in significant_combinations:
		print>>fout,'%s,%s,1'%(combination[0],combination[1])

#Make a colored map
#Color by drug class

#Need to analyze the differences in features, at least to spot check