import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
import csv

from BDD_Service import DatabaseConnection
 
class LoginPage(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("Page de Connexion")
        self.geometry("300x150")


        self.db_connection = DatabaseConnection('localhost', "OGPT", "JadoreOGE", "OGPT")
       

        self.create_widgets()

    def create_widgets(self):
        self.label_surnom = tk.Label(self, text="Surnom:")
        self.label_surnom.pack(pady=5)
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

        if auth_result:
         user_info = auth_result  
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

     
 


class ApplicationEtudiant(tk.Tk):
    def __init__(self, user_info):
        super().__init__()

        self.title("Interface Étudiant")
        self.geometry("600x400")

       
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

        tk.Label(self, text="Nombre d'entretiens :").grid(row=1, column=0, padx=10, pady=10)
        tk.Label(self, text="Nombre d'entreprises :").grid(row=2, column=0, padx=10, pady=10)
        tk.Label(self, text="Note de stage :").grid(row=3, column=0, padx=10, pady=10)
        tk.Label(self, text="Nombre de réponses :").grid(row=4, column=0, padx=10, pady=10)

        self.entretiens_entry = tk.Entry(self, width=30)
        self.entretiens_entry.grid(row=1, column=1, padx=10, pady=10)

        self.nb_entreprises_entry = tk.Entry(self, width=30)
        self.nb_entreprises_entry.grid(row=2, column=1, padx=10, pady=10)

        self.note_stage_entry = tk.Entry(self, width=30)
        self.note_stage_entry.grid(row=3, column=1, padx=10, pady=10)

        self.nb_reponse_entry = tk.Entry(self, width=30)
        self.nb_reponse_entry.grid(row=4, column=1, padx=10, pady=10)

        
        tk.Button(self, text="Valider", command=self.valider_infos).grid(row=6, column=0, columnspan=2, pady=10)

        # Listebox pour afficher les informations
        self.listbox_affichage = tk.Listbox(self, width=60, height=10)
        self.listbox_affichage.grid(row=7, column=0, columnspan=2, padx=10, pady=10)

    def valider_infos(self):
        self.entretiens = self.entretiens_entry.get()
        self.nb_entreprises = self.nb_entreprises_entry.get()
        self.note_stage = self.note_stage_entry.get()
        self.nb_reponse = self.nb_reponse_entry.get()

       
        if not self.nom or not self.prenom or not self.entretiens:
            messagebox.showwarning("Erreur", "Veuillez remplir tous les champs obligatoires.")
            return

      
        self.listbox_affichage.delete(0, tk.END)
        self.listbox_affichage.insert(tk.END, f"Nombre d'entretiens : {self.entretiens}")
        self.listbox_affichage.insert(tk.END, f"Nombre d'entreprises : {self.nb_entreprises}")
        self.listbox_affichage.insert(tk.END, f"Note de stage : {self.note_stage}")
        self.listbox_affichage.insert(tk.END, f"Nombre de réponses : {self.nb_reponse}")

       
        user_id = self.user_info.get('id')
        validate = 0  
        self.db_connection.add_form(user_id, self.nb_entreprises, self.nb_reponse, self.entretiens, validate)

 


class ApplicationAdmin(tk.Tk):
    def __init__(self):
        super().__init__()

        self.etudiants = {}
        self.db_connection = DatabaseConnection('localhost', "OGPT", "JadoreOGE", "OGPT")  
        self.create_widgets()

    def create_widgets(self):
       
        label_bonjour = tk.Label(self, text="Bonjour, Admin!")
        label_bonjour.pack(pady=20)

       
        self.listbox_etudiants = tk.Listbox(self, width=40, height=10)
        self.listbox_etudiants.pack(pady=10)

       
        tk.Button(self, text="Afficher Informations", command=self.afficher_informations).pack(pady=10)

        
        tk.Button(self, text="Ajouter Étudiant", command=self.ajouter_etudiant).pack(pady=10)

        
        tk.Button(self, text="Quitter", command=self.quit).pack()

        
        self.charger_liste_etudiants()

    def ajouter_etudiant(self):
        
        popup = tk.Toplevel(self)
        popup.title("Ajouter Étudiant")
        popup.geometry("300x200")

        # Créer des champs pour le formulaire
        tk.Label(popup, text="Nom Étudiant:").pack(pady=5)
        nom_entry = tk.Entry(popup, width=20)
        nom_entry.pack(pady=5)

        tk.Label(popup, text="Prénom Étudiant:").pack(pady=5)
        prenom_entry = tk.Entry(popup, width=20)
        prenom_entry.pack(pady=5)

        tk.Label(popup, text="Promo:").pack(pady=5)
        promo_var = tk.StringVar()
        promo_var.set("B1")
        promo_menu = tk.OptionMenu(popup, promo_var, "B1", "B2")
        promo_menu.pack(pady=5)

       
        tk.Button(popup, text="Valider", command=lambda: self.valider_etudiant(nom_entry.get(),
                                                                               prenom_entry.get(),
                                                                               promo_var.get(),
                                                                               popup)).pack(pady=10)

    def valider_etudiant(self, nom, prenom, promo, popup):
        
        if not nom or not prenom or not promo:
            messagebox.showwarning("Erreur", "Veuillez remplir tous les champs.")
            return

       
        self.db_connection.add_student(nom, prenom, promo)

       
        self.charger_liste_etudiants()

       
        popup.destroy()

    def charger_liste_etudiants(self):
        
        self.etudiants = self.db_connection.get_all_students()

       
        self.listbox_etudiants.delete(0, tk.END)
        for student_id, student_data in self.etudiants.items():
            self.listbox_etudiants.insert(tk.END, f"{student_data['FirstName']} {student_data['LastName']}")

    def afficher_informations(self):
        
        selection_index = self.listbox_etudiants.curselection()

        
        if not selection_index:
            messagebox.showwarning("Avertissement", "Veuillez sélectionner un étudiant.")
            return

        
        student_id = list(self.etudiants.keys())[selection_index[0]]
        etudiant_selectionne = self.etudiants.get(student_id)

       
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
            tk.Label(popup, text=f"Validation: {'Oui' if form_data['validate'] else 'Non'}").pack(pady=5)


        grade_data = self.db_connection.get_grade_data_for_student(etudiant['ID'])
        if grade_data:
            tk.Label(popup, text=f"IA: {grade_data['IA']}").pack(pady=5)
            tk.Label(popup, text=f"Système: {grade_data['Systeme']}").pack(pady=5)
            tk.Label(popup, text=f"BDD: {grade_data['BDD']}").pack(pady=5)

        tk.Button(popup, text="Ajouter Note", command=lambda: self.ajouter_note(etudiant['ID'])).pack(pady=10)


        
        
      
        
    def ajouter_note(self, user_id):
      
        popup_notes = tk.Toplevel(self)
        popup_notes.title("Ajouter Note")
        popup_notes.geometry("300x200")

        
        tk.Label(popup_notes, text="IA:").pack(pady=5)
        ia_entry = tk.Entry(popup_notes, width=20)
        ia_entry.pack(pady=5)

        tk.Label(popup_notes, text="Système:").pack(pady=5)
        systeme_entry = tk.Entry(popup_notes, width=20)
        systeme_entry.pack(pady=5)

        tk.Label(popup_notes, text="BDD:").pack(pady=5)
        bdd_entry = tk.Entry(popup_notes, width=20)
        bdd_entry.pack(pady=5)

       
        tk.Button(popup_notes, text="Valider", command=lambda: self.valider_notes(user_id, ia_entry.get(), systeme_entry.get(), bdd_entry.get(), popup_notes)).pack(pady=10)

    def valider_notes(self, user_id, ia, systeme, bdd, popup_notes):
        
        if not ia or not systeme or not bdd:
            messagebox.showwarning("Erreur", "Veuillez remplir tous les champs.")
            return

       
        self.db_connection.add_grade_for_student(user_id, ia, systeme, bdd)

       
        popup_notes.destroy()

       
        messagebox.showinfo("Succès", "Notes ajoutées avec succès.")


 
if __name__ == "__main__":
    app_login = LoginPage()
    app_login.mainloop()