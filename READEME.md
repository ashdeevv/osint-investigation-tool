🔍 OSINT Tool — Analyse multi-sources avec scoring de risque
📌 Description

Ce projet est un outil OSINT (Open Source Intelligence) développé en Python, avec interface graphique, permettant d’analyser des usernames, emails et domaines à partir de sources publiques, puis de produire une analyse synthétique avec score de risque.

L’objectif n’est pas seulement de collecter des informations, mais de les corréler, les analyser et les restituer de manière exploitable, comme le ferait un analyste OSINT junior.

🎯 Objectifs du projet

Centraliser plusieurs sources OSINT publiques

Réduire les faux positifs grâce à des règles explicites

Fournir une aide à la décision via un score de risque

Générer un rapport lisible (GUI + PDF)

Respecter un cadre légal et éthique (OSINT passif uniquement)

🚀 Fonctionnalités
🔎 Analyse Username

Recherche multi-plateformes (GitHub, Twitter, Reddit, etc.)

Détection de cohérence d’identité

Recherche de mentions GitHub

Localisation déclarée publiquement (GitHub)

Détection de numéros de téléphone exposés

Score de fiabilité des numéros

Score de risque OSINT global

Résumé exécutif automatique

📧 Analyse Email

Validation de format

Vérification du domaine

Recherche d’exposition sur GitHub

Intégration optionnelle de Have I Been Pwned (API)

🌐 Analyse Domaine

WHOIS

DNS

Reverse DNS

Découverte de sous-domaines (certificats SSL)

🖥️ Interface Graphique (Tkinter)

Analyse multi-cibles

Barre de progression

Mise en couleur du risque (🟢🟠🔴)

Résultats lisibles en temps réel

📄 Export

Rapport texte (.txt)

Rapport structuré (.json)

Export PDF analyste

🧠 Scoring de risque OSINT

Le score est basé sur des règles explicites, par exemple :

Présence multi-plateformes

Exposition email / téléphone

Fiabilité des données trouvées

Surface d’exposition (sous-domaines)

Niveaux :

🟢 Risque faible

🟠 Risque modéré

🔴 Risque élevé

Chaque score est accompagné de justifications claires.

🛠️ Technologies utilisées

Python 3

Tkinter (GUI)

Requests

ReportLab (PDF)

python-dotenv

APIs publiques (GitHub, DNS, WHOIS, HIBP optionnel)

📁 Structure du projet
osint_project/
│
├── gui.py
├── modules/
│   ├── username_search.py
│   ├── email_check.py
│   ├── domain_info.py
│   ├── github_osint.py
│   ├── github_email_osint.py
│   ├── subdomain_osint.py
│   ├── location_osint.py
│   ├── phone_osint.py
│   ├── phone_score.py
│   ├── identity_score.py
│   ├── risk_score.py
│   ├── executive_summary.py
│   └── pdf_report.py
│
├── reports/
│   ├── report.json
│   └── OSINT_Report_*.pdf
│
├── .env
└── README.md

▶️ Installation & lancement
1️⃣ Installer les dépendances
pip install requests reportlab python-dotenv

2️⃣ Lancer l’interface graphique
python3 gui.py

⚠️ Cadre légal & éthique

✔️ Sources publiques uniquement

✔️ OSINT passif

❌ Aucun contournement de sécurité

❌ Aucun accès à des données privées

❌ Aucune exploitation malveillante

Ce projet est strictement éducatif.

🎓 Niveau & usage

Niveau : OSINT Junior → Intermédiaire

Usage :

Apprentissage

Portfolio cybersécurité

Démonstration technique

Projet personnel

📌 Améliorations possibles (futur)

Version web (Flask / FastAPI)

Graphes OSINT

Base de données

Historique des analyses

Authentification

Déploiement

👤 Auteur

Projet développé à des fins éducatives dans une démarche OSINT responsable.