import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
import csv

from services.BDD_Service import DatabaseConnection
from pages.adminPage import ApplicationAdmin
from pages.studentPage import ApplicationEtudiant

class LoginPage(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("Page de Connexion")
        self.geometry("300x200")


        self.db_connection = DatabaseConnection('localhost', "OGPT", "JadoreOGE", "OGPT")

        self.create_widgets()

    def create_widgets(self):
        self.label_surnom = tk.Label(self, text="Surnom:")
        self.label_surnom.pack(pady=(20,5))
        self.entry_surnom = tk.Entry(self)
        self.entry_surnom.pack(pady=5)

        self.label_mot_de_passe = tk.Label(self, text="Mot de Passe:")
        self.label_mot_de_passe.pack(pady=5)
        self.entry_mot_de_passe = tk.Entry(self, show="*")
        self.entry_mot_de_passe.pack(pady=5)

        self.btn_connexion = tk.Button(self, text="Connexion", command=self.connexion)
        self.btn_connexion.pack(pady=10)

    def connexion(self):
        surnom = self.entry_surnom.get()
        mot_de_passe = self.entry_mot_de_passe.get()

        
        auth_result = self.db_connection.auth(surnom, mot_de_passe)

        if auth_result is not None:
         user_info = auth_result  
        else:
            messagebox.showerror("Erreur", "Surnom ou mot de passe incorrect")
            return
        if user_info['Type'] == 'Etudiant':
            self.destroy()
            app_etudiant = ApplicationEtudiant(user_info)
            app_etudiant.mainloop()
        elif user_info['Type'] == 'Admin':
            self.destroy()
            app_admin = ApplicationAdmin()
            app_admin.mainloop()
        else:
            messagebox.showerror("Erreur", "Surnom ou mot de passe incorrect")