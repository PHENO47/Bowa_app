def validate_input(ville, duree):
    errors = []

    if not ville or len(ville.strip()) < 2:
        errors.append("Ville invalide")

    if duree <= 0 or duree > 72:
        errors.append("Durée incohérente")

    return errors