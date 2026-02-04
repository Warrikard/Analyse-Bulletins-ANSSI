# Analyse-Bulletins-ANSSI

Projet de Veille Cyber : Automatisation ANSSI & Enrichissement CVE

# Description
Ce projet automatise la collecte, l'enrichissement et l'analyse des avis et alertes de sécurité publiés par l'ANSSI (CERT-FR). Il identifie les CVE, les enrichit via les API MITRE et FIRST (EPSS), consolide les données dans un fichier CSV et génère des alertes pour les vulnérabilités critiques. On importe les données dans un fichier SQLite via Django qui génère un dashboard web interactif pour la surveillance des vulnérabilités critiques.

## Architecture du Projet

```bash
PROJET_IA_ANSSI/
├── data/                   # Fichier CSV final (donnees.csv)
├── exports/                # Export HTML du Notebook pour le rendu
├── notebooks/              # Notebook d'analyse et visualisations
├── scripts/                # Modules Python métier
│   ├── extraction.py       # Récupère les flux RSS/JSON du CERT-FR.
│   ├── enrichissement.py   # Interroge les API NIST/FIRST (CVSS/EPSS).
│   ├── consolidation.py    # Formate les données pour l'analyse.
│   └── alertes.py          # Filtrage des failles et notifications.
├── config/                 # Application Django (Cœur du projet)
│   ├── management/         # Commandes personnalisées (ex: python manage.py actualiser)
│   ├── templates/          # Interface HTML (dashboard.html)
│   ├── settings.py         # Configuration globale (Apps, DB, Templates)
│   ├── models.py           # Schéma SQL (Vulnerabilite, Bulletin)
│   ├── views.py            # Logique de rendu du dashboard
│   ├── urls.py             # Routage (admin/ et dashboard/)
│   ├── asgi.py/wsgi.py     # Interfaces serveurs
│   └── apps.py             # Configuration de l'application Django
├── manage.py               # Interface de gestion Django (migrations, serveur)
├── db.sqlite3              # Base de données relationnelle locale
├── main.py                 # Script d'exécution global (Pipeline + Django)
├── requirements.txt        # Dépendances (Django, Pandas, Requests)
└── README.md               # Documentation
```

## Installation (Debian 13)

1. **Prérequis système :**

   ```bash
   sudo apt update
   sudo apt install python3-venv python3-pip -y
   ```

2. **Configuration de l'environnement virtuel :**

    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```

3. **Configuration de l'environnement virtuel :**

    ```bash
    pip install -r requirements.txt
    ```
## Utilisation
1. **Extraction et Consolidation :**
Lancez le script principal pour récupérer les données et générer le fichier CSV :

    ```bash
    python3 main.py
    ```

2. Mode Manuel Django
Pour gérer l'interface web indépendamment de l'extraction :

    ```bash
    # Préparation de la base de données
    python3 manage.py makemigrations
    python3 manage.py migrate

    # Importation des données du CSV vers le Dashboard
    python3 manage.py actualiser

    # Lancement du serveur
    python3 manage.py runserver
    ```

3. **Analyse et Visualisation :**
Ouvrir VS Code et lancez le fichier notebooks/analyse_data.ipynb.

-> Sélectionnez le kernel .venv .
-> Exécutez toutes les cellules pour générer les graphiques et le fichier HTML.

## Visualisation du Dashboard
En local : Accédez à http://127.0.0.1:8000/dashboard/

Espace Virtuel (GitHub Codespaces) : 1. Cliquez sur le pop-up "Open in Browser" qui apparaît lors du lancement du serveur. 2. Ajoutez /dashboard/ à la fin de l'URL générée. Exemple : https://votre-id-8000.app.github.dev/dashboard/

## Fonctionnalités Implémentées
Extraction Multi-Flux : Lecture simultanée des Avis et des Alertes.

Enrichissement Complet : Récupération du score CVSS (v2/v3.1/v3.0/v4.0/), du type CWE et du score EPSS.

Analyse de Criticité : Consolidation par bulletin en retenant la vulnérabilité la plus grave.

Système d'Alerte : Détection automatique des menaces avec un score CVSS >= 9.0.

Dashboard Interactif : Visualisation web des vulnérabilités triées par score via API Django.

## Équipe
    Mike CUNHA
    Yasin GUNDOGDU


