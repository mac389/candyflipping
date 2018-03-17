import os
import pandas as pd 
import numpy as np 

from pymongo import MongoClient
from tqdm import tqdm
from collections import Counter 

client = MongoClient()
db = client['candyflipping']
combinations = db['text_by_drug_combinations']


def analyze(distributions):
	 words = distributions['combined'].keys()
	 drugs = list(set(distributions.keys()) - {'unique','combined'})

 	 denominator = {drugs[0]:float(sum(distributions[drugs[0]].values())),
	 				drugs[1]:float(sum(distributions[drugs[1]].values()))}

	 denominator['expected combined'] = denominator[drugs[0]] + denominator[drugs[1]]
	 denominator['actual combined'] = float(sum(distributions['combined'].values()))

	 df = pd.DataFrame(index=words,data=[(distributions[drugs[0]][word],
	 							distributions[drugs[1]][word],
	 							distributions[drugs[1]][word] + distributions[drugs[0]][word],
	 							distributions['combined'][word],
	 							(distributions[drugs[1]][word] + 
	 								distributions[drugs[0]][word])/denominator['expected combined']-distributions['combined'][word]/denominator['actual combined'])
	 						for word in words], 
	 						columns=[drugs[0],drugs[1],'expected combined','actual combined',
	 						'expected-actual'])

	 df /= np.array([denominator[drugs[0]],denominator[drugs[1]],denominator['expected combined'],
	 					denominator['actual combined'],1])


	 df['expected rank'] = df['expected combined'].rank()
	 df['actual rank'] = df['actual combined'].rank()

	 df['actual-expected rank'] = df['actual rank'] - df['expected rank']

	 df.index.name='word'
	 df.sort_values(by='expected-actual',ascending=False).to_csv('./data/%s-%s-normalized'%(drugs[0],drugs[1]))

for item in tqdm(list(combinations.find({'analysis':{"$exists":"true"}})),'Creating DFs'):
	analyze(item['distributions'])
	