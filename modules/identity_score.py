def identity_consistency(username_results):
    total = len(username_results)
    found = sum(1 for v in username_results.values() if v)

    if found == 0:
        return "Aucune présence détectée"
    elif found == 1:
        return "Présence faible (compte isolé)"
    elif found < total / 2:
        return "Présence partielle"
    else:
        return "Présence forte et cohérente"