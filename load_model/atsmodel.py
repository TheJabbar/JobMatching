import joblib

model = joblib.load('*/model/matching-model.pkl')  # Random Forest
vectorizer = joblib.load('*/model/tf-idfvectorizer.pkl')  # TF-IDF

print(type(model))        # <class 'sklearn.ensemble._forest.RandomForestClassifier'>
print(type(vectorizer))   # <class 'sklearn.feature_extraction.text.TfidfVectorizer'>

