from django.db import models

class Bulletin(models.Model):
    titre = models.CharField(max_length=255)
    lien = models.URLField(max_length=500)
    date_publication = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.titre

class Vulnerabilite(models.Model):
    # On lie la vulnérabilité au bulletin
    bulletin = models.ForeignKey(Bulletin, on_delete=models.CASCADE, related_name="cves", null=True)
    cve_id = models.CharField(max_length=50, unique=True)
    cvss = models.FloatField(default=0.0)
    produit = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.cve_id