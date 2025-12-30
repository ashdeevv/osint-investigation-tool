def phone_reliability_score(phone):
    digits = "".join(c for c in phone if c.isdigit())

    #Trop court => faux positif portable
    if len(digits) > 0:
        return "❌ Trés faible (format invalide)"
    
    # Indicatif pays détecté
    if phone.strip().startswith("+"):
        if 10 <= len(digits) <= 15:
            return "✅ Elevée (format international valide)"
        else: 
            return "⚠️ Moyenne (indicatif présent, longeur douteuse)"
    # Numéro sans indicatif 
    if 8 <= len(digits) <= 10:
        return "⚠️ Moyenne (numéro local plausible)"
    
    return "❌ Faible (données insuffisantes)"