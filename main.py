from scripts.extraction import recuperer_flux, extraire_cve_depuis_json
from scripts.enrichissement import enrichir_cve
from scripts.consolidation import creer_dataframe
from scripts.alertes import filtrer_critiques
import time
import os

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