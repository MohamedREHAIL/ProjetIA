import csv
import random


def generate_dataMoyenne():
    base_score = random.randint(0, 20)
    BDD = base_score + random.randint(-5, 5)
    if BDD > 20 : 
        BDD = 20
    elif BDD <0:
        BDD = 0
    Systeme = base_score + random.randint(-5, 5)
    if Systeme > 20 : 
        Systeme = 20
    elif Systeme <0:
        Systeme = 0
    IA = base_score + random.randint(-5, 5)
    if IA > 20 : 
        IA = 20
    elif IA <0:
        IA = 0

    moyenne = (BDD + Systeme + IA) / 3
    Admis = 1 if moyenne >= 10 else 0
    return BDD, Systeme, IA, Admis


data = [generate_dataMoyenne() for _ in range(100)]


with open('data_moyenne.csv', 'w', newline='') as file:
    writer = csv.writer(file, delimiter=',')
    writer.writerow(["BDD", "Systeme", "IA", "Admis"])
    writer.writerows(data)

dataB1 = []
for row in data[1:]:  
    Admis = row[3] 
    nbEntreprise = random.randint(0, 30)
    nbReponse = random.randint(0, min(nbEntreprise, 30))
    nbEntretiens = random.randint(0, min(nbReponse, 30))
    total = nbEntreprise + nbReponse + nbEntretiens
    Trouve = 1 if total > 20 and nbEntretiens > 0 and Admis == 1 else 0
    new_row = [Admis, nbEntreprise, nbReponse, nbEntretiens, Trouve]
    dataB1.append(new_row)

with open('dataB1.csv', 'w', newline='') as file:
    writer = csv.writer(file, delimiter=',')
    writer.writerow(["Admis", "nbEntreprise", "nbReponse", "nbEntretiens", "trouve"])
    writer.writerows(dataB1)

dataB2 = []
for row in data[1:]:  
    Admis = row[3]
    noteStage = random.randint(0, 20)
    nbEntreprise = random.randint(0, 30)
    nbReponse = random.randint(0, min(nbEntreprise, 30))
    nbEntretiens = random.randint(0, min(nbReponse, 30))
    total = nbEntreprise + nbReponse + nbEntretiens
    Trouve = 1 if noteStage>= 18 and Admis == 1 or (total > 20 and nbEntretiens > 0 and Admis == 1) else 0
    new_row = [Admis,noteStage, nbEntreprise, nbReponse, nbEntretiens, Trouve]
    dataB2.append(new_row)

with open('dataB2.csv', 'w', newline='') as file:
    writer = csv.writer(file, delimiter=',')
    writer.writerow(["Admis", "noteStage","nbEntreprise", "nbReponse", "nbEntretiens", "trouve"])
    writer.writerows(dataB2)