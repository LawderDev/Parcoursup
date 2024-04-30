def gale_shapley(men_preferences, women_preferences):
    # Nombre total d'hommes
    num_men = len(men_preferences)
    # Nombre total de femmes
    num_women = len(women_preferences)
    
    # Création d'un dictionnaire pour stocker les appariements homme-femme
    # et leur degré de préférence
    matching = {}
    
    # Création d'un dictionnaire pour stocker les hommes et leur statut actuel
    men_status = {man: None for man in men_preferences.keys()}
    
    # Tant qu'il reste des hommes célibataires
    while None in men_status.values():
        # Choisir un homme célibataire
        man = next(man for man, status in men_status.items() if status is None)
        # Obtenez les préférences de cet homme
        preferences = men_preferences[man]
        # Trouvez la première femme qui n'est pas encore engagée
        for woman in preferences:
            if woman not in matching.values():
                matching[man] = woman
                men_status[man] = "engaged"
                break
            else:
                current_partner = next(man for man, woman in matching.items() if woman == woman)
                current_partner_preference = women_preferences[woman].index(current_partner)
                new_partner_preference = women_preferences[woman].index(man)
                # Si la femme préfère le nouvel homme à l'actuel, effectuez un échange
                if new_partner_preference < current_partner_preference:
                    matching[man] = woman
                    matching[current_partner] = None
                    men_status[man] = "engaged"
                    men_status[current_partner] = None
                    break

    return matching

# Exemple d'utilisation
men_preferences = {
    'John': ['Mary', 'Alice', 'Emma'],
    'Peter': ['Mary', 'Emma', 'Alice'],
    'Mark': ['Alice', 'Mary', 'Emma']
}

women_preferences = {
    'Mary': ['Mark', 'John', 'Peter'],
    'Alice': ['Peter', 'Mark', 'John'],
    'Emma': ['John', 'Peter', 'Mark']
}

matches = gale_shapley(men_preferences, women_preferences)
print(matches)
