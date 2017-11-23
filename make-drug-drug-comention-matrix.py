import json
import numpy as np 
from tqdm import tqdm 

db = json.load(open('./db.json','rb'))

drugs = open('./drugs','rb').read().splitlines()

comention_matrix = np.zeros((len(drugs),len(drugs)))
#iterate over lower triangle
#include diagonal for control

for i,j in tqdm(zip(*np.tril_indices_from(comention_matrix)), 'Comentions'):
	comention_matrix[i,j] = sum([1 if drugs[i] in document["drugs"] and drugs[j] in document["drugs"] else 0
											for document in db.values()])

comention_matrix += comention_matrix.T
comention_matrix[np.diag_indices_from(comention_matrix)]/=2

np.savetxt('./comention-matrix.csv',comention_matrix, delimiter=',',fmt='%d')