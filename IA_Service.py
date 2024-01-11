import numpy as np
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split 
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn import metrics
import pandas as pd
import pickle

def verify(listNotes,listForm, annee):
    notes = pd.DataFrame(listNotes, columns=['BDD','IA','Systeme'])
    with open('moyenne.pkl', 'rb') as f:
        modelMoyenne = pickle.load(f)
    
    admis = modelMoyenne.predict(notes)

    if annee == "B1":
        form = pd.DataFrame([admis[0]] + listForm, columns=['Admis','nbEntreprise','nbReponse', 'nbEntretien'])

        with open('B1.pkl', 'rb') as f:
            modelB1 = pickle.load(f)
        
        result = modelB1.predict(form)
        return result[0]
    else:
        form = pd.DataFrame([admis[0]] + listForm, columns=['Admis','noteStage','nbEntreprise','nbReponse', 'nbEntretien'])

        with open('B2.pkl', 'rb') as f:
            modelB2 = pickle.load(f)
        
        result = modelB2.predict(form)
        return result[0]