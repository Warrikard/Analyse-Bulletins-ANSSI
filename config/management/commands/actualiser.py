import pandas as pd
from django.core.management.base import BaseCommand
from config.models import Vulnerabilite

class Command(BaseCommand):
    def handle(self, *args, **options):
        # Chemin vers ton CSV
        df = pd.read_csv('data/donnees.csv')
        
        # Nettoyage rapide du score
        df['CVSS'] = pd.to_numeric(df['CVSS'], errors='coerce').fillna(0.0)

        for _, row in df.iterrows():
            # Sauvegarde en base de données
            Vulnerabilite.objects.update_or_create(
                cve_id=row['CVE'],
                defaults={
                    'cvss': row['CVSS'],
                    'produit': row['Produit'],
                    'description': row['Description']
                }
            )
        self.stdout.write(self.style.SUCCESS(f"{len(df)} vulnérabilités importées !"))