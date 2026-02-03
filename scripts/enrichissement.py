import requests
import time

def enrichir_cve(cve_id):
    info = {
        "CVE":cve_id, 
        "Organisation d'autorité" : "Inconnu",
        "CVSS": "Inconnu", 
        "Base Severity": "Inconnu", 
        "CWE": "Inconnu", 
        "CWE Description": "Inconnu",
        "EPSS": "Inconnu", 
        "Vendeur" : "Inconnu", 
        "Produit": "Inconnu", 
        "Versions affectées" : "Inconnu", 
        "Description": "Inconnu", 
    }
    try:
        # API MITRE
        url = f"https://cveawg.mitre.org/api/cve/{cve_id}"
        data = requests.get(url, timeout=10).json()
        cna = data["containers"]["cna"]
        adp = data["containers"]["adp"]

        #info["Organisation d'autorité"] = data["cveMetadata"]["assignerShortName"]
        info["Organisation d'autorité"] = data.get("cveMetadata", {}).get("assignerShortName", "Introuvé")

        try:
            metrics = cna.get("metrics", [{}])[0] or adp[0].get("metrics", [{}])[0]
            cvss = metrics.get("cvssV3_1") or metrics.get("cvssV3_0") or metrics.get("cvssV4_0") or metrics.get("cvssV2")
            if cvss:
                info["CVSS"] = cvss.get("baseScore", 0.0)
                info["Base Severity"] = cvss.get("baseSeverity", "N/A")
        except:
            pass
        try:
            problemtype = adp[0].get("problemTypes") or cna.get("problemTypes")
        except:
            pass

        try:
            info["CWE"] = problemtype[0]["descriptions"][0].get("cweId", "Non disponible")
        except:
            pass

        try:
            info["CWE Description"] = problemtype[0]["descriptions"][0].get("description", "Non disponible")
        except:
            pass

        try:
            list_vendeurs = []
            list_p = []
            list_v = []
            affected = data["containers"]["cna"]["affected"]
            for product in affected:
                try:
                    list_vendeurs.append(product.get("vendor", "n/a"))
                    info["Vendeur"] = ", ".join(list_vendeurs)
                except:
                    pass

                try:
                    list_p.append(product.get("product", "n/a"))
                    info["Produit"] = ", ".join(list_p)
                except:
                    pass


                try:
                    for v in product.get("versions", []) :
                        if v.get("status") == "affected":
                            if v.get("version") == "n/a":
                                list_v.append(v.get('version', 'n/a'))
                            else:
                                list_v.append(f"{v.get('version', 'n/a')} - {(v.get('lessThanOrEqual') or v.get('lessThan') or "Fixe")}")
                    info["Versions affectées"] = ", \n".join(list_v)
                except:
                    pass
            
        except:
            pass

        try:
            info["Description"] = data["containers"]["cna"]["descriptions"][0]["value"]
        except:
            pass
        try:
            # API EPSS
            url2 = f"https://api.first.org/data/v1/epss?cve={cve_id}"
            data2 = requests.get(url2, timeout=5).json()
            epss_data = data2.get("data", [])
            if epss_data:
                valeur_brute = float(epss_data[0]["percentile"])
                info["EPSS"] = round(valeur_brute, 2)
        except:
            pass
    except:
        pass
    return info