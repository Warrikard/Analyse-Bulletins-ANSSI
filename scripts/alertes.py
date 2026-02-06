import smtplib
from email.mime.text import MIMEText
import pandas as pd

def send_email(to_email, subject, df_critiques):
    # --- CONFIGURATION ---
    #from_email = "votre_email@gmail.com"
    from_email = "mail_diffusion@gmail.com"
    #password = "votre_mot_de_passe_application"  # 16 caractères de Google
    password = "mdp_app_mail_diffusion"


    # 1. Préparation du texte de l'email
    corps = "ALERTE : Vulnérabilités critiques détectées !\n\n"
    
    for _, row in df_critiques.iterrows():
        corps += f"CVE : {row['CVE']}\n"
        corps += f"Score CVSS : {row['CVSS']}\n"
        corps += f"Produit : {row['Produit']}\n"
        corps += f"Lien : {row['Bulletin_Lien']}\n"
        corps += "-"*30 + "\n"

    # 2. Création de l'objet email
    msg = MIMEText(corps)
    msg['Subject'] = subject
    msg['From'] = from_email
    msg['To'] = to_email

    # 3. Envoi via le serveur Gmail
    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(from_email, password)
            server.sendmail(from_email, to_email, msg.as_string())
        print("✅ Email d'alerte envoyé !")
    except Exception as e:
        print(f"❌ Erreur lors de l'envoi : {e}")

def filtrer_critiques(df, seuil):
    # 1. Conversion forcée en numérique (errors='coerce' transforme le texte invalide en NaN)
    df['CVSS'] = pd.to_numeric(df['CVSS'], errors='coerce')
    
    # 2. On remplace les valeurs vides (NaN) par 0.0 pour éviter les bugs
    df['CVSS'] = df['CVSS'].fillna(0.0)
    
    # 3. Maintenant la comparaison fonctionne car on compare float >= float
    critiques = df[df['CVSS'] >= seuil].copy()
    
    if not critiques.empty:
        print(f"⚠️ {len(critiques)} failles critiques trouvées !")
        send_email("destinataire@gmail.com", "Test Alerte Sécurité", critiques)
    else:
        print("✅ Aucune faille au dessus du seuil.")
    return critiques

