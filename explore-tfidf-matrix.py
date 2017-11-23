import json, itertools 
import numpy as np 

from scipy.stats import scoreatpercentile
from tqdm import tqdm 
db = json.load(open('./tf-idf-matrix.json','rb'))

print db["lsa"].items()
scores = []
#what are the top %10 most discriminating words?
for drug in tqdm(db.keys(), "Drugs"):
	scores += [db[drug].values()]

scores = list(itertools.chain.from_iterable(scores))
print scores
cutoff = 85
print cutoff

#filter list
filtered_tf_idf = {}
for drug in tqdm(db.keys(),"Filtering Keywords"):
	filtered_tf_idf[drug] = {key:value for key,value in db[drug].iteritems() if value > cutoff}

json.dump(filtered_tf_idf,open('./filtered_tf_idf_matrix.json','wb'))
