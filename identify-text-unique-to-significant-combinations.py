import itertools

from pymongo import MongoClient
from tqdm import tqdm
from collections import Counter 

client = MongoClient()
db = client['candyflipping']
combinations = db['text_by_drug_combinations']
single_drugs = db['text_by_drug']

calculate_distribution = lambda text: dict(Counter(text.split()))

list_of_drugs = open('./significant-combinations').read().splitlines()

for entry in tqdm(list_of_drugs,'Iterating through combinations'):
	d1,d2 = entry.split('_')

	if d1 != d2: #only combinations of unique drugs

		try:
			post = list(combinations.find({"drugs":{"$all":[d1,d2]}}))[0]

			combined_text = post['text']
			combined_distribution = calculate_distribution(combined_text)

			d1_text = list(single_drugs.find({"drug":d1}))[0]['text']
			d1_distribution = calculate_distribution(d1_text)

			d2_text = list(single_drugs.find({"drug":d2}))[0]['text']
			d2_distribution = calculate_distribution(d2_text)

			unique = {word:count for word,count in combined_distribution.items()
							if word not in d1_distribution and word not in d2_distribution}

			'''
			post['distributions'] = {"combined":combined_distribution,
									 d1:d1_distribution,
									 d2:d2_distribution,
									 "unique":unique}
			'''

			post['distributions']['unique'] = unique
			combinations.save(post)
		except:
			print d1,d2