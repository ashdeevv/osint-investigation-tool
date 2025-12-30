from modules.username_search import search_username
from modules.check_email import check_email
from modules.domain_info import get_domain_info, get_dns_info
from dotenv import load_dotenv
from modules.hibp_check import check_email_breaches
import os
import json
from datetime import datetime

def main():
    # Charger les variables d'environement (.env)
    load_dotenv()

    # === Entrées utilisateur ===
    username = input("Username à rechercher : ")
    email = input("Email à analyser : ")
    domain = input("Domaine à analyser : ")

    # === Appels OSINT ===
    username_results = search_username(username)
    email_results = check_email(email)
    domain_results = get_domain_info(domain)
    dns_results = get_dns_info(domain)

    # === HIBP (optionnel) ===
    hibp_api_key = os.getenv("HIBP_API_KEY")

    if hibp_api_key:
        hibp_results = check_email_breaches(email)
    else: 
        hibp_results = {
            "enabled": False, 
            "message": "HIBP non activé (clé API manquantes)"
        }

    # === Construction du rapport texte ===
    report = "\n=== RAPPORT OSINT ===\n\n"

    report += "🔍 Username:\n"
    for site, found in username_results.items():
        report += f" - {site}: {'Trouvé' if found else 'Non trouvé'}\n"

    report += "\n📧 Email:\n"
    for key, value in email_results.items():
        report += f" - {key}: {value}\n"

    report += "\n🌐 Domaine (WHOIS):\n"
    for key, value in domain_results.items():
        report += f" - {key}: {value}\n"

    report += "\n🌍 DNS:\n"
    for key, value in dns_results.items():
        report += f" - {key}: {value}\n"
    
    # === Section HIBP ===
    report += "\n🔥 Fuites de données (Have I Been Pwend):\n"

    if hibp_results.get("enable") is False:
        report += "- HIBP non activé (clé API absente)\n"
    elif hibp_results.get("breached"):
        report += "- Email compromis ❌\n"
        for breach in hibp_results["breaches"]:
            report += f"• {breach['name']} ({breach['date']})\n"
            report += f"     Données : {', '.join(breach['data'])}\n"
    else: 
        report += " - Aucune fuite connue ✅\n"

    # === Sauvegarde TXT ===
    with open("reports/report.txt", "w", encoding="utf-8") as f:
        f.write(report)

    # === Sauvegarde JSON (pro / exploitable) ===
    with open("reports/report.json", "w", encoding="utf-8") as f:
        json.dump(
            {
                "timestamp": datetime.now().isoformat(),
                "username": username_results,
                "email": email_results,
                "domain": domain_results,
                "dns": dns_results,
            },
            f,
            indent=4
        )

    # === Affichage console ===
    print(report)

if __name__ == "__main__":
    main()