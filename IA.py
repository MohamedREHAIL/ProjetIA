import numpy as np
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split 
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn import metrics
import pandas as pd
import pickle



def moyenne (test_size, random_state):
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
    print(accuracy)
    with open('moyenne.pkl', 'wb') as f:
        pickle.dump(regressor, f)

def TroisA (test_size, random_state):
    if test_size == 1.0 :
        return
    
    df = pd.read_csv('data3.csv')

    X = df[['Admis', 'noteStage', 'nbEntreprise','nbEntretiens']]
    y = df['trouve']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)

    regressor = LogisticRegression()  
    regressor.fit(X_train, y_train)

    y_pred = regressor.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(accuracy)
    with open('3A.pkl', 'wb') as f:
        pickle.dump(regressor, f)

def DeuxA (test_size, random_state):
    if test_size == 1.0 :
        return
    
    df = pd.read_csv('data2.csv')

    X = df[['Admis', 'nbEntreprise','nbEntretiens']]
    y = df['trouve']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)

    regressor = LogisticRegression()  
    regressor.fit(X_train, y_train)

    y_pred = regressor.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(accuracy)
    with open('2A.pkl', 'wb') as f:
        pickle.dump(regressor, f)

moyenne(0.3,0)
TroisA(0.5,0)
DeuxA(0.5,0)