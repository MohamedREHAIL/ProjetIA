import numpy as np
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split 
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn import metrics
import pandas as pd
import pickle

test_size_score = 0
max_accuracy = 0

def moyenne (test_size, random_state):
    global test_size_score, max_accuracy
    if test_size == 1.0 :
        return
    
    df = pd.read_csv('data.csv')

    X = df[['BDD', 'Systeme', 'IA']]
    y = df['Admis']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)

    regressor = LogisticRegression()  
    regressor.fit(X_train, y_train)

    y_pred = regressor.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)

    if accuracy <= max_accuracy :
        moyenne(test_size+0.1,0)
    else:
        test_size_score = test_size
        max_accuracy = accuracy
        with open('model.pkl', 'wb') as f:
            pickle.dump(regressor, f)

moyenne(0.3,0)