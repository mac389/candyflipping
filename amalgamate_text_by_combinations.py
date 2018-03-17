import itertools

from pymongo import MongoClient
from tqdm import tqdm
from pprint import pprint 

client = MongoClient()
db = client['candyflipping']
collection = db['lycaeum']
combinations = db['text_by_drug']
only_combinations = db['text_by_drug_combinations']
list_of_drugs = open('./drugs','rb').read().splitlines()

for drug_one,drug_two in tqdm(list(itertools.combinations(list_of_drugs,2)),"Finding Text Specific to Combinations"):
	text_in_drug_one = list(combinations.find({"drug":drug_one}))[0]['text']
	text_in_drug_two = list(combinations.find({"drug":drug_two}))[0]['text']

	text_in_one_two_combination = [' '.join(item['data']['processed_text'])
							for item in collection.find({}) if drug_one in item['data']['drugs']
							and drug_two in item['data']['drugs']]


	if text_in_one_two_combination:
		text_in_one_two_combination = ' '.join(text_in_one_two_combination)
		payload = {"drugs":[drug_one,drug_two],"text":text_in_one_two_combination}
		only_combinations.insert_one(payload)

#13861 potential combinations, of those 5679 had text 