def calculate_risk_score(
    identity_score,
    email_exposed=False,
    hibp_breached=False,
    phone_scores=None,
    subdomain_count=0
):
    """
    Retourne (niveau_risque, score, raisons)
    """

    score = 0
    reasons = []

    # === Identité ===
    if identity_score:
        if "forte" in identity_score.lower():
            score += 2
            reasons.append("Présence multi-plateformes cohérente")
        elif "faible" in identity_score.lower():
            score += 1
            reasons.append("Présence isolée")

    # === Email ===
    if email_exposed:
        score += 2
        reasons.append("Email exposé publiquement")

    if hibp_breached:
        score += 3
        reasons.append("Email présent dans des fuites de données")

    # === Téléphone ===
    if phone_scores:
        for p in phone_scores:
            if "Élevée" in p["score"]:
                score += 3
                reasons.append("Numéro de téléphone fiable exposé")
                break
            elif "Moyenne" in p["score"]:
                score += 1
                reasons.append("Numéro de téléphone plausible exposé")
                break

    # === Domaine ===
    if subdomain_count >= 5:
        score += 2
        reasons.append("Surface de domaine étendue (sous-domaines)")

    # === Décision finale ===
    if score >= 7:
        return "🔴 Risque ÉLEVÉ", score, reasons
    elif score >= 4:
        return "🟠 Risque MODÉRÉ", score, reasons
    else:
        return "🟢 Risque FAIBLE", score, reasons