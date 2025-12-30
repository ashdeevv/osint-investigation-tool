import tkinter as tk
from tkinter import messagebox, scrolledtext, ttk

from modules.username_search import search_username
from modules.check_email import check_email
from modules.domain_info import get_domain_info, get_dns_info
from modules.hibp_check import check_email_breaches

from modules.github_osint import search_github_username
from modules.github_email_osint import search_github_email
from modules.subdomain_osint import find_subdomains
from modules.identity_score import identity_consistency
from modules.location_osint import search_location_from_github
from modules.phone_osint import search_phone_in_github
from modules.phone_score import phone_reliability_score
from modules.risk_score import calculate_risk_score
from modules.executive_summary import generate_executive_summary
from modules.pdf_report import generate_pdf_report

from dotenv import load_dotenv
import os
import json
from datetime import datetime

load_dotenv()

# ---------- Helpers ----------
def parse_lines(widget):
    return [l.strip() for l in widget.get("1.0", tk.END).splitlines() if l.strip()]

def insert_risk_text(widget, text, risk_level):
    if "FAIBLE" in risk_level:
        widget.insert(tk.END, text, "risk_low")
    elif "MODÉRÉ" in risk_level:
        widget.insert(tk.END, text, "risk_medium")
    elif "ÉLEVÉ" in risk_level:
        widget.insert(tk.END, text, "risk_high")
    else:
        widget.insert(tk.END, text)

def export_pdf():
    try:
        report_text = output.get("1.0", tk.END)

        if not report_text.strip():
            messagebox.showwarning("PDF", "Aucun rapport à exporter")
            return
        filename = f"reports/OSINT_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        generate_pdf_report(filename, report_text)

        messagebox.showinfo("PDF", f"Raport PDF généré :\n{filename}")
    except Exception as e:
        messagebox.showerror("Erreur PDF", str(e))

# ---------- Main OSINT ----------
def run_osint():
    usernames = parse_lines(text_usernames)
    emails = parse_lines(text_emails)
    domains = parse_lines(text_domains)

    if not usernames and not emails and not domains:
        messagebox.showerror("Erreur", "Ajoute au moins une cible")
        return

    output.delete("1.0", tk.END)
    progress["value"] = 0
    root.update_idletasks()

    total_steps = len(usernames) + len(emails) + len(domains)
    step = 100 / max(total_steps, 1)

    report = "\n=== RAPPORT OSINT AVANCÉ ===\n\n"
    json_report = {
        "timestamp": datetime.now().isoformat(),
        "usernames": {},
        "emails": {},
        "domains": {}
    }

    # ===== USERNAMES =====
    for username in usernames:
        output.insert(tk.END, f"\n🔍 USERNAME : {username}\n")

        username_results = search_username(username)
        identity = identity_consistency(username_results)
        github_mentions = search_github_username(username)
        location = search_location_from_github(username)
        phones = search_phone_in_github(username)

        phones_scored = [
            {"number": p, "score": phone_reliability_score(p)}
            for p in phones
        ]

        risk_level, risk_score, risk_reasons = calculate_risk_score(
            identity_score=identity,
            email_exposed=False,
            hibp_breached=False,
            phone_scores=phones_scored,
            subdomain_count=0
        )

        summary = generate_executive_summary(risk_level, risk_reasons)

        json_report["usernames"][username] = {
            "platforms": username_results,
            "identity_score": identity,
            "location": location,
            "phones_scored": phones_scored,
            "github_mentions": github_mentions,
            "risk": {
                "level": risk_level,
                "score": risk_score,
                "reasons": risk_reasons
            },
            "executive_summary": summary
        }

        for site, found in username_results.items():
            output.insert(tk.END, f" - {site}: {'Trouvé' if found else 'Non trouvé'}\n")

        output.insert(tk.END, f" 🧠 Cohérence identité : {identity}\n")
        output.insert(tk.END, f" 📍 Localisation (OSINT) : {location}\n")

        if phones_scored:
            output.insert(tk.END, " 📞 Numéros exposés publiquement:\n")
            for p in phones_scored:
                output.insert(tk.END, f"   • {p['number']} → {p['score']}\n")
        else:
            output.insert(tk.END, " 📞 Aucun numéro exposé détecté\n")

        output.insert(tk.END, "\n 🧠 RÉSUMÉ EXÉCUTIF :\n")
        output.insert(tk.END, f" {summary}\n")

        output.insert(tk.END, "\n 🎯 SCORE DE RISQUE OSINT : ")
        insert_risk_text(
            output,
            f"{risk_level} ({risk_score}/10)\n",
            risk_level
        )

        output.insert(tk.END, " 📌 Raisons :\n")
        for r in risk_reasons:
            output.insert(tk.END, f"   • {r}\n")

        progress["value"] += step
        root.update_idletasks()

    # ===== EMAILS =====
    for email in emails:
        output.insert(tk.END, f"\n📧 EMAIL : {email}\n")

        email_validation = check_email(email)
        github_email_hits = search_github_email(email)

        json_report["emails"][email] = {
            "validation": email_validation,
            "github_exposure": github_email_hits
        }

        for k, v in email_validation.items():
            output.insert(tk.END, f" - {k}: {v}\n")

        if github_email_hits:
            output.insert(tk.END, " 🐙 Email exposé sur GitHub:\n")
            for hit in github_email_hits:
                output.insert(tk.END, f"   • {hit['repo']} → {hit['url']}\n")
        else:
            output.insert(tk.END, " 🐙 Aucune exposition GitHub détectée\n")

        hibp_key = os.getenv("HIBP_API_KEY")
        if hibp_key:
            hibp = check_email_breaches(email)
            json_report["emails"][email]["hibp"] = hibp

            if hibp.get("breached"):
                output.insert(tk.END, " 🔥 Fuites HIBP détectées ❌\n")
            else:
                output.insert(tk.END, " 🔥 Aucune fuite HIBP connue ✅\n")

        progress["value"] += step
        root.update_idletasks()

    # ===== DOMAINES =====
    for domain in domains:
        output.insert(tk.END, f"\n🌐 DOMAINE : {domain}\n")

        whois_info = get_domain_info(domain)
        dns_info = get_dns_info(domain)
        subdomains = find_subdomains(domain)

        json_report["domains"][domain] = {
            "whois": whois_info,
            "dns": dns_info,
            "subdomains": subdomains
        }

        for k, v in whois_info.items():
            output.insert(tk.END, f" - {k}: {v}\n")

        for k, v in dns_info.items():
            output.insert(tk.END, f" - {k}: {v}\n")

        if subdomains:
            output.insert(tk.END, " 🌍 Sous-domaines détectés:\n")
            for sub in subdomains[:10]:
                output.insert(tk.END, f"   • {sub}\n")

        progress["value"] += step
        root.update_idletasks()

    with open("reports/report.json", "w", encoding="utf-8") as f:
        json.dump(json_report, f, indent=4)

    progress["value"] = 100

# ================= UI =================
root = tk.Tk()
root.title("OSINT Tool – Niveau 2 (Score & Couleurs)")
root.geometry("1150x900")

tk.Label(root, text="Usernames (1 par ligne)").pack()
text_usernames = scrolledtext.ScrolledText(root, width=130, height=5)
text_usernames.pack()

tk.Label(root, text="Emails (1 par ligne)").pack()
text_emails = scrolledtext.ScrolledText(root, width=130, height=5)
text_emails.pack()

tk.Label(root, text="Domaines (1 par ligne)").pack()
text_domains = scrolledtext.ScrolledText(root, width=130, height=5)
text_domains.pack()

tk.Button(
    root,
    text="Lancer l’analyse OSINT avancée",
    command=run_osint
).pack(pady=15)

tk.Button(
    root,
    text="Exporter le raport en PDF",
    command=lambda: export_pdf()
).pack(pady=5)

progress = ttk.Progressbar(
    root,
    orient="horizontal",
    length=800,
    mode="determinate"
)
progress.pack(pady=10)

output = scrolledtext.ScrolledText(root, width=160, height=35)
output.pack(pady=10)

# ===== Tags couleur =====
output.tag_config("risk_low", foreground="#2ecc71")     # Vert
output.tag_config("risk_medium", foreground="#f39c12")  # Orange
output.tag_config("risk_high", foreground="#e74c3c")    # Rouge

root.mainloop()