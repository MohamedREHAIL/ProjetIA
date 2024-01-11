import mysql.connector
import hashlib
from enum import Enum
import pandas as pd

from services.IA_Service import verify

def hash(query):
    hasher = hashlib.sha256()

    hasher.update(query.encode('utf-8'))

    hash_output = hasher.hexdigest()

    return hash_output

class Promo(Enum):
    B1 = "B1"
    B2 = "B2"

class DatabaseConnection:
   
    def __init__(self, host_name, user_name, user_password, db_name):
        self.connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name
        )
        self.cursor = self.connection.cursor()

    def auth(self, username, password):
        try:
            hashPassword = hash(password)
            values = (username, hashPassword)
            self.cursor.execute("SELECT * FROM User WHERE username=%s AND password=%s", values)
            result = self.cursor.fetchone()  
            if result:
                return {'id':result[0],'Type': result[1], 'FirstName': result[2], 'LastName': result[3]} 
            else:
                return None
        except Exception as e:
            print(f"The error '{e}' occurred")
            return None

    def add_student(self, nom, prenom, username, password, userListId):
        try:
            
            hashed_password = hash(password)

           
            insert_user_query = "INSERT INTO User (Type, FirstName, LastName, username, password, UserList_id) VALUES (%s, %s, %s, %s, %s, %s)"
            user_values = ('Etudiant', nom, prenom, username, hashed_password, userListId)
            self.cursor.execute(insert_user_query, user_values)

           
            self.connection.commit()

            print("Étudiant ajouté avec succès.")
        except Exception as e:
            
            self.connection.rollback()
            print(f"L'erreur suivante s'est produite : {e}")

    def add_form(self, user_id, nb_entreprise, nb_reponse, nb_entretien, validate):
        try:
            
            insert_form_query = "INSERT INTO Form (userId, nbEntreprise, nbReponse, nbEntretien, validate) VALUES (%s, %s, %s, %s, %s)"
            form_values = (user_id, nb_entreprise, nb_reponse, nb_entretien, validate)
            self.cursor.execute(insert_form_query, form_values)

            
            self.connection.commit()

            print("Form added successfully.")
        except Exception as e:
            
            self.connection.rollback()
            print(f"The following error occurred: {e}")
            return -1
        return 0

    def get_all_students(self, userListId):
            try:
                self.cursor.execute("SELECT U.*, UL.promo FROM User U JOIN UserList UL ON U.UserList_id = UL.id WHERE UL.id = %s", (userListId,))
                students = self.cursor.fetchall()

                student_dict = {}
                for student in students:
                    student_dict[student[0]] = {
                        'ID':student[0],
                        'Type': student[1],
                        'FirstName': student[2],
                        'LastName': student[3],
                        'Username': student[4],
                        'Password': student[5],
                        'UserList_id': student[6],
                        'Promo': student[7], 
                    }

                return student_dict
            except Exception as e:
                print(f"The error '{e}' occurred")
                return {}
    
    def get_form_data_for_student(self, user_id):
        try:
            self.cursor.execute("SELECT * FROM Form WHERE userId = %s", (user_id,))
            form_data = self.cursor.fetchone()

            if form_data:
                return {
                    'userId': form_data[1],
                    'nbEntreprise': form_data[2],
                    'nbReponse': form_data[3],
                    'nbEntretien': form_data[4],
                    'validate': form_data[5],
                }
            else:
                return None
        except Exception as e:
            print(f"The error '{e}' occurred")
            return None
        
    def add_grade_for_student(self, user_id, ia, systeme, bdd, stage):
        try:
            if stage:
                insert_grade_query = "INSERT INTO Grade (userId, IA, Systeme, BDD, Stage) VALUES (%s, %s, %s, %s, %s)"
                grade_values = (user_id, ia, systeme, bdd, stage)
                self.cursor.execute(insert_grade_query, grade_values)
                self.connection.commit()
            else:
                insert_grade_query = "INSERT INTO Grade (userId, IA, Systeme, BDD) VALUES (%s, %s, %s, %s)"
                grade_values = (user_id, ia, systeme, bdd)
                self.cursor.execute(insert_grade_query, grade_values)
                self.connection.commit()
            print("Notes ajoutées avec succès.")
        except Exception as e:
            self.connection.rollback()
            print(f"L'erreur suivante s'est produite : {e}")
    
    def get_grade_data_for_student(self, user_id):
        try:
            self.cursor.execute("SELECT * FROM Grade WHERE userId = %s", (user_id,))
            form_data = self.cursor.fetchone()

            if form_data:
                return {
                    'userId': form_data[1],
                    'IA': form_data[2],
                    'Systeme': form_data[3],
                    'BDD': form_data[4],
                    
                }
            else:
                return None
        except Exception as e:
            print(f"The error '{e}' occurred")
            return None

    def get_Userlists(self):
        try:
            self.cursor.execute("SELECT UL.*, COUNT(U.id) FROM UserList AS UL LEFT JOIN User AS U ON U.UserList_id = UL.id GROUP BY UL.id")
            userLists = self.cursor.fetchall()
            userList_dict = {}
            for userList in userLists:
                userList_dict[userList[0]] = {
                    'ID':userList[0],
                    'Promo': userList[1],
                    'Name': userList[2],
                    'NbEtud': userList[3], 
                }
            return userList_dict
        except Exception as e:
            print(f"The error '{e}' occurred")
            return {}

    def addUserList(self, name, promo):
        try: 
            insert_user_query = "INSERT INTO UserList (name, promo) VALUES (%s, %s)"
            if promo == Promo.B1:
                values = (name, "B1")
            else:
                values = (name, "B2")
            self.cursor.execute(insert_user_query, values)

           
            self.connection.commit()

            print("UserList ajouté avec succès.")
        except Exception as e:
            self.connection.rollback()
            print(f"L'erreur suivante s'est produite : {e}")

    def validate(self, user_id, promo, ia, systeme, bdd, stage, nb_entreprise, nb_reponse, nb_entretien):
        try:
            result = verify(ia,bdd,systeme,stage,nb_entreprise, nb_reponse, nb_entretien, promo)
            insert_user_query = "UPDATE `Form` SET `validate` = %s WHERE userId=%s;"
            values = (int(result),user_id)
            self.cursor.execute(insert_user_query, values)

            
            self.connection.commit()
            print("UserList ajouté avec succès.")
        except Exception as e:
            self.connection.rollback()
            print(f"L'erreur suivante s'est produite : {e}")
            print("coucou")



    def close_connection(self):
        self.connection.close()
        print("Connection closed")

