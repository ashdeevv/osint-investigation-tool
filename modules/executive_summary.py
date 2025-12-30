def generate_executive_summary(risk_level, reasons):
    if "FAIBLE" in risk_level:
        return (
            "Ce profil présente une exposition OSINT faible."
            "Aucune information sensible critique n'a été detectée."
        )
    if "MODÉRÉ" in risk_level:
        return (
            "Ce profil présente une exposition OSINT modérée. "
            "Certaines information publiques peuvent nécessiter une vigilance accrue."
        )
    if "ÉLEVÉ" in risk_level:
        reasons_text = ", ".join(reasons[:2])
        return (
            "Ce profil présente une exposition OSINT élevée. "
            f"Facteurs pricipeaux : {reasons_text}."
        )
    return "Résumé exécutif indisponibele"