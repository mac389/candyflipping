import itertools

import numpy as np 

from pymongo import MongoClient
from tqdm import tqdm
from collections import Counter 
from scipy.stats import chi2_contingency


client = MongoClient()
db = client['candyflipping']
combinations = db['text_by_drug_combinations']
single_drugs = db['text_by_drug']


list_of_drugs = open('./significant-combinations').read().splitlines()
#624 significant combinations, of 5267 total combinations
for entry in tqdm(list_of_drugs,'Iterating through combinations'):
	d1,d2 = entry.split('_')

	if d1 != d2:
		post = list(combinations.find({"drugs":{"$all":[d1,d2]}}))[0]
		#chi-square test
		#expected frequency is d1 + d2

		all_combined_words = post['distributions']['combined'].keys()
		combined_common_words = np.array([[post['distributions']['combined'][word], 
								post['distributions'][d1][word] + post['distributions'][d1][word]]
								for word in all_combined_words
				if all([word in post['distributions'][d1].keys(),
						word in post['distributions'][d2].keys()])], dtype=int)

		#drop words that occurred less than five times
		combined_common_words = combined_common_words[np.all(combined_common_words>5,axis=1),:]

		chi,p,_,_ = chi2_contingency(combined_common_words)
		post['analysis'] = {'observed-expected':combined_common_words.tolist(),
							'test':{'chi':chi,'p-value':p}}

		combinations.save(post)
		#unique words
		if post['distributions']['unique']:
			print post['distributions']['unique']