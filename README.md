# Analyse-Bulletins-ANSSI

Projet de Veille Cyber : Automatisation ANSSI & Enrichissement CVE

## Description
Ce projet automatise la collecte, l'enrichissement et l'analyse des avis et alertes de sécurité publiés par l'ANSSI (CERT-FR). Il identifie les CVE, les enrichit via les API MITRE et FIRST (EPSS), consolide les données dans un fichier CSV et génère des alertes pour les vulnérabilités critiques.

## Architecture du Projet
PROJET_IA_ANSSI/
├── data/                   # Fichier CSV final (donnees_consolidees.csv)
├── exports/                # Export HTML du Notebook pour le rendu
├── notebooks/              # Notebook d'analyse et visualisations
├── scripts/                # Modules Python (Extraction, Enrichissement, etc.)
├── main.py                 # Script principal d'exécution
├── requirements.txt        # Dépendances Python
└── README.md               # Documentation

## Installation (Debian 13)

1. **Prérequis système :**
   ```bash
   sudo apt update
   sudo apt install python3-venv python3-pip -y
   ```

2. **Configuration de l'environnement virtuel :**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3. **Configuration de l'environnement virtuel :**
    ```bash
    
    ```

## Utilisation
1. **Extraction et Consolidation :**
Lancez le script principal pour récupérer les données et générer le fichier CSV :
    ```bash
    python3 main.py
    ```

2. **Analyse et Visualisation :**
Ouvrir VS Code et lancez le fichier notebooks/analyse_data.ipynb.

-> Sélectionnez le kernel venv.
-> Exécutez les cellules pour générer les graphiques (Histogrammes CVSS, Scatter plots EPSS).

3. **Génération du livrable HTML :**
Dans le Notebook, faites File > Export As > HTML et placez le résultat dans le dossier exports/.

## Fonctionnalités Implémentées
Extraction Multi-Flux : Lecture simultanée des Avis et des Alertes.

Enrichissement Complet : Récupération du score CVSS (v3.1/v3.0/v4.0), du type CWE et du score EPSS.

Analyse de Criticité : Consolidation par bulletin en retenant la vulnérabilité la plus grave (CVSS Max).

Système d'Alerte : Détection automatique des menaces avec un score CVSS >= 9.0.


## Équipe
    Mike CUNHA
    Yasin GUNDOGDU

pip install -r requirements.txt