import json, nltk 

from tqdm import tqdm
from sklearn.feature_extraction.text import TfidfVectorizer

db = json.load(open('./text-by-drug.json','rb'))
stopwords = open('./general-stopwords').read().splitlines()

drugs, corpus = zip(*db.items())
corpus = [' '.join(item) for item in corpus]
#preprocess corpus

tf = TfidfVectorizer(ngram_range=(1,3), min_df = 0, stop_words = stopwords,
						 analyzer='word')


tfidf_matrix =  tf.fit_transform(corpus)
print 'Made matrix'
feature_names = tf.get_feature_names() 


dense = tfidf_matrix.todense()
print 'Converted to dense'
#print dense[0].tolist()[0]
#Get indexes of nonzero

#central_matrix = {drug:{feature_names[idx]:dense[i][0,idx] for idx in dense[i].nonzero()[1]} 
#									for i,drug in enumerate(drugs)}

central_matrix = {}
for i,drug in tqdm(enumerate(drugs),'Drugs'):
	central_matrix[drug] = {feature_names[idx]:dense[i][0,idx] for idx in dense[i].nonzero()[1]}	

json.dump(central_matrix,open('./tf-idf-matrix.json','wb'))