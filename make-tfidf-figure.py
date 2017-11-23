import json, nltk 

from sklearn.feature_extraction.text import TfidfVectorizer

db = json.load(open('./text-by-drug.json','rb'))
stopwords = open('./general-stopwords').read().splitlines()

drugs, corpus = zip(*db.items())

#preprocess corpus

tf = TfidfVectorizer(ngram_range=(1,3), min_df = 0, stop_words = stopwords,
						 analyzer='word')

tfidf_matrix =  tf.fit_transform(corpus)
feature_names = tf.get_feature_names() 


dense = tfidf_matrix.todense()
#print dense[0].tolist()[0]
#Get indexes of nonzero
central_matrix = {drug:{feature_names[idx]:dense[i][0,idx] for idx in dense[i].nonzero()[1]} 
									for i,drug in enumerate(drugs)}

json.dump(central_matrix,open('./tf-idf-matrix.json','wb'))