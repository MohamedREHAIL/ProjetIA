import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
from tkinter import ttk
import csv

from services.BDD_Service import DatabaseConnection

class PageTwo(tk.Toplevel):
    def __init__(self, idUserList, promo):
        super().__init__()
        self.userlist = idUserList
        self.etudiants = {}
        self.db_connection = DatabaseConnection('localhost', "OGPT", "JadoreOGE", "OGPT")  
        self.create_widgets()

    def create_widgets(self):
       
        self.listbox_etudiants = ttk.Treeview(self)
        self.listbox_etudiants.bind('<Double-1>', self.on_double_click)
        self.listbox_etudiants.pack(pady=10)
        self.listbox_etudiants["columns"]=("nom")
        self.listbox_etudiants.column("#0", width=0, stretch=tk.NO)
        self.listbox_etudiants.column("nom", width=100)
        self.listbox_etudiants.heading("nom", text="Nom")
        
        tk.Button(self, text="Ajouter Étudiant", command=self.ajouter_etudiant).pack(pady=10)


        
        self.charger_liste_etudiants()

    def ajouter_etudiant(self):
        
        popup = tk.Toplevel(self)
        popup.title("Ajouter Étudiant")
        popup.geometry("300x300")

        # Créer des champs pour le formulaire
        tk.Label(popup, text="Nom Étudiant:").pack(pady=5)
        nom_entry = tk.Entry(popup, width=20)
        nom_entry.pack(pady=5)

        tk.Label(popup, text="Prénom Étudiant:").pack(pady=5)
        prenom_entry = tk.Entry(popup, width=20)
        prenom_entry.pack(pady=5)

        tk.Label(popup, text="Username:").pack(pady=5)
        username_entry = tk.Entry(popup, width=20)
        username_entry.pack(pady=5)

        tk.Label(popup, text="Mot de passe:").pack(pady=5)
        mdp_entry = tk.Entry(popup, width=20,show="*")
        mdp_entry.pack(pady=5)


       
        tk.Button(popup, text="Valider", command=lambda: self.valider_etudiant(nom_entry.get(),
                                                                               prenom_entry.get(),
                                                                               username_entry.get(),
                                                                               mdp_entry.get(),
                                                                               popup)).pack(pady=10)

    def valider_etudiant(self, nom, prenom,username, password, popup):
        
        if not nom or not prenom or not username or not password:
            messagebox.showwarning("Erreur", "Veuillez remplir tous les champs.")
            return

       
        self.db_connection.add_student(nom, prenom,username,password,self.userlist)

       
        self.charger_liste_etudiants()

       
        popup.destroy()

    def charger_liste_etudiants(self):
        
        self.etudiants = self.db_connection.get_all_students(self.userlist)

        for item in self.listbox_etudiants.get_children():
            self.listbox_etudiants.delete(item)
        for student_id, student_data in self.etudiants.items():
            name = f"{student_data['FirstName']} {student_data['LastName']}"
            self.listbox_etudiants.insert("", "end", iid=student_id ,values=(name))

    def on_double_click(self,event):
        
        selected = self.listbox_etudiants.selection()[0]
        etudiant_selectionne = self.etudiants.get(int(selected))
        print(etudiant_selectionne)
       
        self.afficher_details_etudiant(etudiant_selectionne)

    def afficher_details_etudiant(self, etudiant):
        
        popup = tk.Toplevel(self)
        popup.title("Informations Étudiant")
        popup.geometry("300x300")

        
        tk.Label(popup, text=f"Nom: {etudiant['FirstName']}").pack(pady=5)
        tk.Label(popup, text=f"Prénoms: {etudiant['LastName']}").pack(pady=5)
        tk.Label(popup, text=f"Promo: {etudiant['Promo']}").pack(pady=5)

       
        form_data = self.db_connection.get_form_data_for_student(etudiant['ID'])
        if form_data:
            tk.Label(popup, text=f"Nombre d'entreprises: {form_data['nbEntreprise']}").pack(pady=5)
            tk.Label(popup, text=f"Nombre de réponses: {form_data['nbReponse']}").pack(pady=5)
            tk.Label(popup, text=f"Nombre d'entretiens: {form_data['nbEntretien']}").pack(pady=5)
            


        grade_data = self.db_connection.get_grade_data_for_student(etudiant['ID'])
        if grade_data:
            tk.Label(popup, text=f"IA: {grade_data['IA']}").pack(pady=5)
            tk.Label(popup, text=f"Système: {grade_data['Systeme']}").pack(pady=5)
            tk.Label(popup, text=f"BDD: {grade_data['BDD']}").pack(pady=5)
            if form_data:
                tk.Label(popup, text=f"Trouve une alternance: {'Oui' if form_data['validate'] else 'Non'}").pack(pady=5)

        if form_data:
            tk.Button(popup, text="Ajouter Note", command=lambda: self.ajouter_note(etudiant['ID'], etudiant['Promo'],form_data['nbEntreprise'],form_data['nbEntretien'],form_data['nbReponse'])).pack(pady=10)
        else:
            tk.Label(popup, text="En attente de l'envoi du formulaire").pack(pady=5)
        
    def ajouter_note(self, user_id, promo, nb_entreprise, nb_entretien, nb_reponse):
      
        popup_notes = tk.Toplevel(self)
        popup_notes.title("Ajouter Note")
        popup_notes.geometry("300x300")

        
        tk.Label(popup_notes, text="IA:").pack(pady=5)
        ia_entry = tk.Entry(popup_notes, width=20)
        ia_entry.pack(pady=5)

        tk.Label(popup_notes, text="Système:").pack(pady=5)
        systeme_entry = tk.Entry(popup_notes, width=20)
        systeme_entry.pack(pady=5)

        tk.Label(popup_notes, text="BDD:").pack(pady=5)
        bdd_entry = tk.Entry(popup_notes, width=20)
        bdd_entry.pack(pady=5)

        if promo == "B2":
            tk.Label(popup_notes, text="Stage:").pack(pady=5)
            stage_entry = tk.Entry(popup_notes, width=20)
            stage_entry.pack(pady=5)
            tk.Button(popup_notes, text="Valider", command=lambda: self.valider_notes(user_id, promo, ia_entry.get(), systeme_entry.get(), bdd_entry.get(), stage_entry.get(),nb_entretien, nb_entreprise, nb_reponse, popup_notes)).pack(pady=10)
        else:
            tk.Button(popup_notes, text="Valider", command=lambda: self.valider_notes(user_id, promo, ia_entry.get(), systeme_entry.get(), bdd_entry.get(), None,nb_entretien, nb_entreprise, nb_reponse, popup_notes)).pack(pady=10)

    def valider_notes(self, user_id, promo, ia, systeme, bdd, stage, nb_entretien, nb_entreprise, nb_reponse, popup_notes):
        
        if promo == "B2" and (not ia or not systeme or not bdd or not stage):
            messagebox.showwarning("Erreur", "Veuillez remplir tous les champs.")
            return
        elif promo == "B1" and (not ia or not systeme or not bdd):
            messagebox.showwarning("Erreur", "Veuillez remplir tous les champs.")
            return

       
        self.db_connection.add_grade_for_student(user_id, ia, systeme, bdd,stage)

        self.db_connection.validate(user_id,promo,ia,systeme, bdd, stage,nb_entreprise, nb_reponse, nb_entretien)

       
        popup_notes.destroy()

       
        messagebox.showinfo("Succès", "Notes ajoutées avec succès.")

class ApplicationAdmin(tk.Tk):
    def __init__(self):
        super().__init__()
        self.db_connection = DatabaseConnection('localhost', "OGPT", "JadoreOGE", "OGPT")
        self.listUser={}
        self.create_widgets()
    
    def on_double_click(self,event):
        # Obtenez l'élément sélectionné
        selected = self.tree.selection()[0]
        item = self.tree.item(selected)  # Obtenez les informations de l'élément
        classe = item['values'][1]
        # Ouvrez une nouvelle fenêtre avec l'ID de la liste d'étudiants
        new_window = PageTwo(selected, classe)
        
    def create_widgets(self):
       
        label_bonjour = tk.Label(self, text="Bonjour, Admin!")
        label_bonjour.pack(pady=20)

       
        self.tree = ttk.Treeview(self)
        self.tree.bind('<Double-1>', self.on_double_click)
        self.tree.pack(pady=10)
        self.tree["columns"]=("nom","classe", "nombre_etudiants")
        self.tree.column("#0", width=0, stretch=tk.NO)
        self.tree.column("classe", width=100)
        self.tree.column("nom", width=200)
        self.tree.column("nombre_etudiants", width=100)
        self.tree.heading("classe", text="Classe")
        self.tree.heading("nom", text="Nom")
        self.tree.heading("nombre_etudiants", text="Nombre d'étudiants")

        tk.Button(self, text="Ajouter Groupe", command=lambda: self.nouveauGroupe()).pack(pady=10)

        
        tk.Button(self, text="Quitter", command=lambda: self.quit()).pack()

        
        self.charger_liste_etudiants()

    def nouveauGroupe(self):
        popup = tk.Toplevel(self)
        popup.title("Ajouter Groupe")
        popup.geometry("300x200")

        # Créer des champs pour le formulaire
        tk.Label(popup, text="Nom :").pack(pady=5)
        nom_entry = tk.Entry(popup, width=20)
        nom_entry.pack(pady=5)

        tk.Label(popup, text="Promo:").pack(pady=5)
        promo_var = tk.StringVar()
        promo_var.set("B1")
        promo_menu = tk.OptionMenu(popup, promo_var, "B1", "B2")
        promo_menu.pack(pady=5)

       
        tk.Button(popup, text="Valider", command=lambda: self.valider_Groupe(nom_entry.get(),
                                                                               promo_var.get(),
                                                                               popup)).pack(pady=10)

    def valider_Groupe(self, nom, promo, popup):
        if not nom or not promo:
            messagebox.showwarning("Erreur", "Veuillez remplir tous les champs.")
            return
        self.db_connection.addUserList(nom, promo)
        self.charger_liste_etudiants()
        popup.destroy()

    def charger_liste_etudiants(self):
        print("chargement...")
        self.listUser = self.db_connection.get_Userlists()

        for item in self.tree.get_children():
            self.tree.delete(item)
        for list_id, list_data in self.listUser.items():
            self.tree.insert("", "end", iid=list_id ,values=(list_data["Name"], list_data["Promo"], list_data["NbEtud"]))