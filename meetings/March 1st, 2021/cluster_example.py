# -*- coding: utf-8 -*-
"""
Created on Sun Feb 21 12:02:45 2021

@author: Arjun
"""

from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import pandas as pd

# returns a dictinoary where the key is the cluster, and the value is a list of all the indices in the cluster
def get_clusters(k, labels):
    results = {}

    for i in range(k):
        results[i] = [] # create empty list 

    for i in range(len(labels)):
        label = labels[i]
        results[label].append(i)
    
    return results

data = pd.read_csv('./country_data.csv') # read in data from csv file
data = data.dropna()
print(data)

### Different ways to cluster the data set
# data = data.iloc[:, 1:] # cluster entire data set
# data = data.iloc[:, 2:6] # cluster based on first 5 columns
data_life_exp = data['life_expec'] # cluster based on life expectancy
data_life_exp = data_life_exp.to_numpy().reshape(-1, 1) # convert to numpy array for algorithm
data_life_exp = data_life_exp[0:16] # use first 15 rows

k = 5 # 5 clusters
model = KMeans(n_clusters=k) # KMeans

# run cluster algorithm, labels will contain the cluster value for each point in the dataset given to the model
labels = model.fit_predict(data_life_exp)

print("Cluster Label for each data point:")
print(labels)
print()

results = get_clusters(k, labels)
print("Cluster with the indicies from the dataset")
print(results)
print()

for i in results: 
    indices = results[i]
    print("Cluster: ", i)
    
    for index in indices: # print all of the countries in the cluster
        country = data.iloc[index] # get row of data from index
        
        print("Country %s with life expectancy %.1f" %(country['country'], country['life_expec']))
    
    print()

