import json, itertools 

from tqdm import tqdm 
from pprint import pprint 
db = json.load(open('./db.json','rb'))
drugs = open('./drugs','rb').read().splitlines()


drug_text = {}
drug_text = {drug: list(itertools.chain.from_iterable([entry['processed_text'] 
				for entry in db.itervalues() if drug in entry['drugs']])) 
				for drug in drugs}

json.dump(drug_text,open('./text-by-drug.json','wb'))