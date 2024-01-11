import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
import csv

from services.BDD_Service import DatabaseConnection

class ApplicationEtudiant(tk.Tk):
    def __init__(self, user_info):
        super().__init__()

        self.title("Interface Étudiant")
        self.geometry("350x400")

       
        self.db_connection = DatabaseConnection('localhost', "OGPT", "JadoreOGE", "OGPT")
        self.user_info = user_info
        self.nb_entreprises = 0
        self.nb_entretiens = 0
        self.note_stage = 0
        self.nb_reponse = 0

        self.nom = user_info.get('FirstName', '')
        self.prenom = user_info.get('LastName', '')
        self.create_widgets()

    def create_widgets(self):
        greeting_label = tk.Label(self, text=f"Bonjour {self.nom} {self.prenom}!")
        greeting_label.grid(row=0, column=0, columnspan=2, pady=10)

        intro_label = tk.Label(self, text=f"Vous allez répondre a un questionnaire pour savoir l'avancement sur votre recherche d'alternance, veuillez completer ces 3 champs :", wraplength=300)
        intro_label.grid(row=1, column=0, columnspan=2, pady=10)

        
        tk.Label(self, text="Nombre d'entreprises contactées:", wraplength=100).grid(row=2, column=0, padx=10, pady=10)
        tk.Label(self, text="Nombre de réponses obtenues (meme les refus):", wraplength=100).grid(row=3, column=0, padx=10, pady=10)
        tk.Label(self, text="Nombre d'entretiens :", wraplength=100).grid(row=4, column=0, padx=10, pady=10)

        

        self.nb_entreprises_entry = tk.Entry(self, width=30)
        self.nb_entreprises_entry.grid(row=2, column=1, padx=10, pady=10)

        self.nb_reponse_entry = tk.Entry(self, width=30)
        self.nb_reponse_entry.grid(row=3, column=1, padx=10, pady=10)

        self.entretiens_entry = tk.Entry(self, width=30)
        self.entretiens_entry.grid(row=4, column=1, padx=10, pady=10)

        
        tk.Button(self, text="Valider", command=self.valider_infos).grid(row=6, column=0, columnspan=2, pady=10)

    def valider_infos(self):
        self.entretiens = self.entretiens_entry.get()
        self.nb_entreprises = self.nb_entreprises_entry.get()
        self.nb_reponse = self.nb_reponse_entry.get()

       
        if not self.nom or not self.prenom or not self.entretiens or not self.nb_entreprises or not self.nb_reponse:
            messagebox.showwarning("Erreur", "Veuillez remplir tous les champs obligatoires.")
            return

        user_id = self.user_info.get('id')
        validate = 0  
        result = self.db_connection.add_form(user_id, self.nb_entreprises, self.nb_reponse, self.entretiens, validate)
        if result == -1:
            messagebox.showwarning("Erreur", "Une erreur s'est produite, veuillez réessayer plus tard")
        else:
            messagebox.showinfo("Formulaire envoyé", "Merci, votre formulaire a été envoyé")
            

