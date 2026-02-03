import pandas as pd

def creer_dataframe(donnees):
    lignes_pour_dataframe = []

    for b in donnees:        
        for cve in b.get('CVE_IDs', []):
            # On crée une ligne plate : Titre du bulletin + les infos de la CVE
            #print(f"{b['Titre']} , {cve}")
            nouvelle_ligne = {
                "Bulletin_Titre": b["Type"] +": \n"+ b['Titre'],
                "Bulletin_Lien": b['Lien Bulletin'],
                "Bulletin_Date": b['Date']
            } | cve
            lignes_pour_dataframe.append(nouvelle_ligne)
        
    df = pd.DataFrame(lignes_pour_dataframe)
    # Sauvegarde dans le dossier data/
    df.to_csv("data/donnees.csv", index=False)
    return df