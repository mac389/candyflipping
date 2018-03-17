import itertools

from pymongo import MongoClient
from tqdm import tqdm

client = MongoClient()
db = client['candyflipping']
collection = db['lycaeum']
combinations = db['text_by_drug']

list_of_drugs = open('./drugs').read().splitlines()
for drug in tqdm(list_of_drugs, "Amalgamating text"):

	text  = ' '.join(list(itertools.chain.from_iterable([item["data"]["processed_text"]
					for item in collection.find({}) if drug in item["data"]["drugs"]])))

	combinations.insert_one({"drug":drug,"text":text})