from django.shortcuts import render
from .models import Vulnerabilite

def dashboard(request):
    # On récupère les CVE par score décroissant
    cves = Vulnerabilite.objects.all().order_by('-cvss')
    return render(request, 'dashboard.html', {'vulnerabilites': cves})