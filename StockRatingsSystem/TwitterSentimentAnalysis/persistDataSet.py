import pickle
from sklearn.datasets import load_files

#nltk.download('stopwords')

#Import Dataset -> generate two classes one each for each sub directorties 
dataset = load_files('txt_sentoken/')

X,y = dataset.data, dataset.target

#store as pickle file, these are byte type file

with open('X.pickle', 'wb') as f:
    pickle.dump(X,f)
    
with open('y.pickle', 'wb') as f:
    pickle.dump(y,f)