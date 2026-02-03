from scripts.extraction import recuperer_flux, extraire_cve_depuis_json
from scripts.enrichissement import enrichir_cve
from scripts.consolidation import creer_dataframe
from scripts.alertes import filtrer_critiques
import time
import os
import subprocess

# Création des dossiers si absents
for d in ['data', 'exports', 'notebooks']:
    if not os.path.exists(d): os.makedirs(d)

print("Extraction ANSSI...")
bulletins = recuperer_flux()

print("1. Extraction JSON...")
for b in bulletins:
    #print(f"Analyse : {b['Titre']}")
    cves = extraire_cve_depuis_json(b['Lien Bulletin'])
    #print(f"{cves}")
    b['CVE_IDs']=[]
    #list_c = []
    for c in cves:
        infos_cve = enrichir_cve(c)
        b['CVE_IDs'].append(infos_cve)
        #list_c.append(enrichir_cve(c))
        time.sleep(0.01)
    #b['CVE_IDs'] = list_c
    #print(b['CVE_IDs'])

print("2. Consolidation...")
df = creer_dataframe(bulletins)

print("3. Alertes...")
filtrer_critiques(df, 9.0)

print("Terminé. Fichier dispo dans data/donnees_consolidees.csv")


# --- Commandes DJANGO ---
print("\n--- Mise à jour de l'interface Web ---")

try:
    # Préparation des migrations (cyber_app est le label défini dans ton apps.py)
    print("Mise à jour des schémas...")
    subprocess.run(["python3", "manage.py", "makemigrations"], check=True)

    # Application des migrations
    print("Application des changements à la base de données...")
    subprocess.run(["python3", "manage.py", "migrate"], check=True)

    # Import des nouvelles données vers SQLite
    print("Importation des données CVE vers le dashboard...")
    subprocess.run(["python3", "manage.py", "actualiser"], check=True)

    # Lancement du serveur
    print("\nLancement du serveur Dashboard sur http://127.0.0.1:8000/dashboard/")
    subprocess.run(["python3", "manage.py", "runserver"])

except subprocess.CalledProcessError as e:
    print(f"Erreur lors de l'exécution d'une commande Django : {e}")
except KeyboardInterrupt:
    print("\nArrêt du serveur par l'utilisateur.")