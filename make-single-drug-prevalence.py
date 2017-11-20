import json, itertools

import matplotlib.pyplot as plt 
import pandas as pd 
import seaborn as sns

from pprint import pprint 
from collections import Counter 

db = json.load(open('./db.json','rb'))

drugs = list(itertools.chain.from_iterable([entry['drugs'] for entry in db.itervalues()]))
drug_frequencies = dict(Counter(drugs)).items()



df = pd.DataFrame.from_dict(drug_frequencies)
df.columns = ["substance","count"]
df.sort_values(by="count",inplace=True, ascending=False)
df.to_csv('./single-drug-frequencies.csv', index=False)


fig = plt.figure()
ax = fig.add_subplot(111)
sns.barplot(y='substance',x='count',data=df.head(20), ax =ax, color='k')


# Add a legend and informative axis label
ax.set(ylabel="",
       xlabel="No. of mentions of substance")
sns.despine(left=True, bottom=True) 
plt.tight_layout()
plt.savefig('./single-drug-frequency.png')