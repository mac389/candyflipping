import os

import pandas as pd 
import matplotlib.pyplot as plt 

for filename in os.listdir('./data')[:3]:
	if 'normalized' in filename:
		df = pd.read_csv(os.path.join('.','data',filename))
		
		#10 words whose ranking increased the most
		more_popular_words = df.sort_values(by='actual-expected rank').head(10)

		#10 words whose ranking decreased the most
		less_popular_words = df.sort_values(by='actual-expected rank').tail(10)[::-1]

		print more_popular_words