import re
import nltk
import pickle
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix
from sklearn.feature_extraction.text import TfidfVectorizer

nltk.download('stopwords')

with open('X.pickle', 'rb') as f:
    X=pickle.load(f)
    
with open('y.pickle', 'rb') as f:
    y=pickle.load(f)
    
corpus = []

for i in range(0,len(X)):
    data = re.sub(r'\W', ' ', str(X[i]))
    data = data.lower()
    data = re.sub(r'\s+[a-z]\s+', ' ', data)
    data = re.sub(r'^[a-z]\s+', ' ', data)
    data = re.sub(r'\s+', ' ', data)
    corpus.append(data)
    
#create BOW, max_features = len(X) -> some fixed number of most frequent words as features and exclude other
#min_df = 3, exclude the word if the same is appearing less than some number of documents
#max_df =0.6, exclude the word if the same is appearing more than 60% of documents, frequent words like the etc
#stopwords.words('english'), excludes all the stop words as per nltk 
vectorizer = CountVectorizer(stop_words=stopwords.words('english'), max_df = 0.6, min_df = 3, max_features = len(X))

X = vectorizer.fit_transform(corpus).toarray()#will generate 2D array [len(X),len(X)], total number of docs = number of features = len(x)

# convert BOW to TF-IDF
transformer = TfidfTransformer()
X = transformer.fit_transform(X).toarray()

#print(X)

text_train,text_test,sentiment_train,sentiment_test = train_test_split(X,y,test_size=0.2,random_state=0)#80% training and 20% testing data
# text_train is training set documents, text_test is test set documents
# sentiment_train is sentiment class for each corresponding training set documents, sentiment_test is sentiment class for each corresponding test set documents


# create the classifier using logistic regression
classifier = LogisticRegression()
classifier.fit(text_train,sentiment_train)

#testing model performance
sentiment_prediction = classifier.predict(text_test)
cm = confusion_matrix(sentiment_test,sentiment_prediction)# [[predicted as 0 and actually 0, predicted as 0 and actually 1],[predicted as 1 and actually 0, predicted as 1 and actually 1]]


print("accuracy : ", (cm[0][0]+cm[1][1])/(cm[0][0]+cm[0][1]+cm[1][0]+cm[1][1])*100,"%")
'''
[model predicted 0and actual 0      model predicted 1 nand actual 0
model predicted 1 and actual 0      model predicted 1 and actual 1]
'''
#store the classifier ....pickle file

with open('classifier.pickle', 'wb') as f:
    pickle.dump(classifier,f)

#store the TFIDF vectorizer
vectorizerTFIDF = TfidfVectorizer(stop_words=stopwords.words('english'), max_df = 0.6, min_df = 3, max_features = len(X))
X_TDIDF = vectorizerTFIDF.fit_transform(corpus).toarray()

with open('vectorizerTFIDF.pickle', 'wb') as f:
    pickle.dump(vectorizerTFIDF,f)
