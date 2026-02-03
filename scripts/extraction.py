import feedparser
import requests
import re

def recuperer_flux():
    urls = [
        "https://www.cert.ssi.gouv.fr/avis/feed/",
        "https://www.cert.ssi.gouv.fr/alerte/feed/"
    ]
    liste_bulletins = []
    for url in urls:
        feed = feedparser.parse(url)
        for entry in feed.entries:
            liste_bulletins.append({
                "Titre": entry.title,
                "Lien Bulletin": entry.link,
                "Date": entry.published,
                "Type": "Alerte" if "/alerte/" in url else "Avis"
            })
            # pour les tests => sortir apres la premiere entree 
            #break
    return liste_bulletins

def extraire_cve_depuis_json(lien_bulletin):
    json_url = f"{lien_bulletin}json/"
    try:
        data = requests.get(json_url)
        if data.status_code == 200:
            return list(set(re.findall(r"CVE-\d{4}-\d{4,7}", str(data.json()))))
    except:
        return []
    return []