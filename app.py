import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
import csv
 
class LoginPage(tk.Tk):
    def __init__(self):
        super().__init__()
 
        self.title("Page de Connexion")
        self.geometry("300x150")
        self.entreprises=[]
 
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
 
        # Vérifier le rôle de l'utilisateur (étudiant ou admin)
        if surnom == "etudiant" and mot_de_passe == "password_etudiant":
            self.destroy()  # Fermer la fenêtre de connexion
            app_etudiant = ApplicationEtudiant()
            app_etudiant.mainloop()
        elif surnom == "admin" and mot_de_passe == "password_admin":
            self.destroy()  # Fermer la fenêtre de connexion
            app_admin = ApplicationAdmin()
            app_admin.mainloop()
        else:
            messagebox.showerror("Erreur", "Surnom ou mot de passe incorrect")
 


class ApplicationEtudiant(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Interface Étudiant")
        self.geometry("600x400")

        self.entreprises = []
        self.zones_recherche = []
        self.nom = ""
        self.prenom = ""
        self.entretiens = ""

        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="Nom :").grid(row=0, column=0, padx=10, pady=10)
        tk.Label(self, text="Prénoms :").grid(row=1, column=0, padx=10, pady=10)
        tk.Label(self, text="Nombre d'entretiens :").grid(row=2, column=0, padx=10, pady=10)

        self.nom_entry = tk.Entry(self, width=30)
        self.nom_entry.grid(row=0, column=1, padx=10, pady=10)

        self.prenom_entry = tk.Entry(self, width=30)
        self.prenom_entry.grid(row=1, column=1, padx=10, pady=10)

        self.entretiens_entry = tk.Entry(self, width=30)
        self.entretiens_entry.grid(row=2, column=1, padx=10, pady=10)

        # Bouton pour valider les informations
        tk.Button(self, text="Valider", command=self.valider_infos).grid(row=3, column=0, columnspan=2, pady=10)

        # Listebox pour afficher les entreprises et les zones de recherche
        self.listbox_affichage = tk.Listbox(self, width=60, height=10)
        self.listbox_affichage.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

        # Champ de saisie pour ajouter une entreprise
        self.entreprise_entry = tk.Entry(self, width=30)
        self.entreprise_entry.grid(row=5, column=0, padx=10, pady=10)

        # Bouton pour ajouter une entreprise
        tk.Button(self, text="Ajouter entreprise", command=self.ajouter_entreprise).grid(row=5, column=1, pady=10)

        # Champ de saisie pour ajouter une zone de recherche
        self.zone_recherche_entry = tk.Entry(self, width=30)
        self.zone_recherche_entry.grid(row=6, column=0, padx=10, pady=10)

        # Bouton pour ajouter une zone de recherche
        tk.Button(self, text="Ajouter zone de recherche", command=self.ajouter_zone_recherche).grid(row=6, column=1, pady=10)

        # Bouton pour sauvegarder les informations dans un fichier CSV
        tk.Button(self, text="Sauvegarder CSV", command=self.sauvegarder_csv).grid(row=7, column=0, columnspan=2, pady=10)

    def valider_infos(self):
        self.nom = self.nom_entry.get()
        self.prenom = self.prenom_entry.get()
        self.entretiens = self.entretiens_entry.get()

        # Vérifier si les champs obligatoires sont vides
        if not self.nom or not self.prenom or not self.entretiens:
            messagebox.showwarning("Erreur", "Veuillez remplir tous les champs obligatoires.")
            return

    def ajouter_entreprise(self):
        entreprise = self.entreprise_entry.get()

        # Vérifier si le champ est vide
        if not entreprise:
            messagebox.showwarning("Erreur", "Veuillez remplir le champ d'entreprise.")
            return

        # Ajouter l'entreprise à la liste
        self.entreprises.append((self.nom, self.prenom, self.entretiens, entreprise))

        # Mettre à jour la listebox
        self.maj_listbox_affichage()

        # Effacer le champ de saisie
        self.entreprise_entry.delete(0, tk.END)

    def ajouter_zone_recherche(self):
        zone_recherche = self.zone_recherche_entry.get()

        # Vérifier si le champ est vide
        if not zone_recherche:
            messagebox.showwarning("Erreur", "Veuillez remplir le champ de zone de recherche.")
            return

        # Ajouter la zone de recherche à la liste
        self.zones_recherche.append(zone_recherche)

        # Mettre à jour la listebox
        self.maj_listbox_affichage()

        # Effacer le champ de saisie
        self.zone_recherche_entry.delete(0, tk.END)

    def maj_listbox_affichage(self):
        # Effacer la listebox
        self.listbox_affichage.delete(0, tk.END)

        # Ajouter les entreprises à la listebox
        for entreprise in self.entreprises:
            self.listbox_affichage.insert(tk.END, f"Nom : {entreprise[0]}, Prénoms : {entreprise[1]}, "
                                                  f"Entretiens : {entreprise[2]}, Entreprise : {entreprise[3]}")

        # Ajouter les zones de recherche à la listebox
        for zone_recherche in self.zones_recherche:
            self.listbox_affichage.insert(tk.END, f"Zone de recherche : {zone_recherche}")

    def sauvegarder_csv(self):
        # Nom du fichier CSV
        fichier_csv = "informations_etudiants.csv"

        # Ouvrir le fichier en mode append ('a') pour ajouter un nouvel étudiant
        with open(fichier_csv, mode='a', newline='') as csvfile:
            # Créer un objet writer pour écrire dans le fichier CSV
            writer = csv.writer(csvfile)

            # Récupérer les informations de l'étudiant
            nom = self.entreprises[0][0]
            prenom = self.entreprises[0][1]
            entretiens = self.entreprises[0][2]

            # En-tête du fichier CSV (si le fichier est vide)
            if csvfile.tell() == 0:
                writer.writerow(["Nom", "Prénoms", "Entretiens", "Entreprise", "Zone de recherche"])

            # Écrire les informations de l'étudiant dans le fichier CSV
            for entreprise in self.entreprises:
                writer.writerow([nom, prenom, entretiens, entreprise[0], ""])
            
            # Écrire les informations des zones de recherche (si disponibles)
            for zone_recherche in self.zones_recherche:
                writer.writerow([nom, prenom, entretiens, entreprise, zone_recherche])

        messagebox.showinfo("Sauvegarde CSV", "Les informations ont été ajoutées dans le fichier CSV.")

 


class ApplicationAdmin(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Interface Admin")
        self.geometry("400x400")

        self.etudiants = {}
        self.create_widgets()

    def create_widgets(self):
        # Ajoutez des éléments à votre interface admin
        label_bonjour = tk.Label(self, text="Bonjour, Admin!")
        label_bonjour.pack(pady=20)

        # Listebox pour afficher la liste des étudiants
        self.listbox_etudiants = tk.Listbox(self, width=40, height=10)
        self.listbox_etudiants.pack(pady=10)

        # Bouton pour afficher les informations de l'étudiant sélectionné
        tk.Button(self, text="Afficher Informations", command=self.afficher_informations).pack(pady=10)

        # Bouton pour quitter l'application
        tk.Button(self, text="Quitter", command=self.quit).pack()

        # Charger la liste des étudiants depuis le fichier CSV
        self.charger_liste_etudiants()

    def charger_liste_etudiants(self):
        # Nom du fichier CSV
        fichier_csv = "informations_etudiants.csv"

        try:
            with open(fichier_csv, mode='r') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    nom_prenom = f"{row['Nom']} {row['Prénoms']}"
                    if nom_prenom not in self.etudiants:
                        self.etudiants[nom_prenom] = {
                            'Nom': row['Nom'],
                            'Prénoms': row['Prénoms'],
                            'Entretiens': row['Entretiens'],
                            'Entreprises': [],
                            'Zones de recherche': []
                        }
                    else:
                        # Ajouter les entreprises et les zones de recherche aux étudiants redondants
                        self.etudiants[nom_prenom]['Entreprises'].append(row['Entreprise'])
                        self.etudiants[nom_prenom]['Zones de recherche'].append(row['Zone de recherche'])

        except FileNotFoundError:
            messagebox.showerror("Erreur", "Le fichier CSV n'a pas été trouvé.")

        # Remplir la listebox avec les noms des étudiants
        for etudiant in self.etudiants.values():
            self.listbox_etudiants.insert(tk.END, f"{etudiant['Nom']} {etudiant['Prénoms']}")

    def afficher_informations(self):
        # Récupérer l'index de l'étudiant sélectionné dans la listebox
        selection_index = self.listbox_etudiants.curselection()

        # Vérifier si un étudiant est sélectionné
        if not selection_index:
            messagebox.showwarning("Avertissement", "Veuillez sélectionner un étudiant.")
            return

        # Récupérer les informations de l'étudiant sélectionné
        nom_prenom_selectionne = self.listbox_etudiants.get(selection_index[0])
        etudiant_selectionne = self.etudiants[nom_prenom_selectionne]

        # Créer la chaîne d'informations à afficher dans la popup
        informations_texte = (
            f"Nom: {etudiant_selectionne['Nom']}\n"
            f"Prénoms: {etudiant_selectionne['Prénoms']}\n"
            f"Nombre d'entretiens: {etudiant_selectionne['Entretiens']}\n"
            f"Entreprises:\n {', '.join(etudiant_selectionne['Entreprises'])}\n"
            f"Zones de recherche:\n {', '.join(etudiant_selectionne['Zones de recherche'])}"
        )

        # Afficher la popup avec les informations
        messagebox.showinfo("Informations Étudiant", informations_texte)




 
if __name__ == "__main__":
    app_login = LoginPage()
    app_login.mainloop()