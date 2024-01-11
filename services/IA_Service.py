import numpy as np
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split 
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn import metrics
import pandas as pd
import pickle

def verify(ia, bdd, systeme, stage,nb_entreprise, nb_reponse, nb_entretien, annee):
    try:
        notes = pd.DataFrame({'BDD': [bdd], 'Systeme': [systeme], 'IA': [ia]})
        with open('moyenne.pkl', 'rb') as f:
            modelMoyenne = pickle.load(f)
        
        admis = modelMoyenne.predict(notes)
    except Exception as e:
        print("ici 1")

    try:
        if annee == "B1":
            form = pd.DataFrame({'Admis' : [admis[0]], 'nbEntreprise': [nb_entreprise],'nbReponse' : [nb_reponse],'nbEntretiens': [nb_entretien]})

            with open('B1.pkl', 'rb') as f:
                modelB1 = pickle.load(f)
            
            result = modelB1.predict(form)
            return result[0]
        else:
            form = pd.DataFrame({'Admis' : [admis[0]], 'noteStage': [stage], 'nbEntreprise': [nb_entreprise],'nbReponse' : [nb_reponse],'nbEntretiens': [nb_entretien]})

            with open('B2.pkl', 'rb') as f:
                modelB2 = pickle.load(f)
            
            result = modelB2.predict(form)
            return result[0]
    except Exception as e:
        print("ici 2")