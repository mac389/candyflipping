import json 
from pymongo import MongoClient
from tqdm import tqdm

client = MongoClient()
db = client['candyflipping']
collection = db['lycaeum']

db = json.load(open('/Users/mac389/Dropbox/db.json','rb'))
for key,value in tqdm(db.items(),'Populated MongoDB with Lycaeum Data'):
	collection.insert_one({"title":key,"data":value})
