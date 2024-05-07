import timeit

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
                woman_to_check = woman
                current_partner = next(man for man, woman in matching.items() if woman == woman_to_check)
                current_partner_preference = women_preferences[woman_to_check].index(current_partner)
                new_partner_preference = women_preferences[woman_to_check].index(man)
                # Si la femme préfère le nouvel homme à l'actuel, effectuez un échange
                if new_partner_preference < current_partner_preference:
                    matching[man] = woman_to_check
                    matching[current_partner] = None
                    men_status[man] = "engaged"
                    men_status[current_partner] = None
                    break

    return matching

# Exemple d'utilisation
men_preferences = {'m1': ['w3', 'w4', 'w5', 'w1', 'w2'], 
                   'm2': ['w3', 'w4', 'w2', 'w5', 'w1'], 
                   'm3': ['w3', 'w4', 'w1', 'w2', 'w5'], 
                   'm4': ['w5', 'w4', 'w2', 'w3', 'w1'], 
                   'm5': ['w3', 'w1', 'w4', 'w5', 'w2']}
women_preferences = {'w1': ['m3', 'm2', 'm5', 'm1', 'm4'], 
                     'w2': ['m3', 'm1', 'm5', 'm4', 'm2'], 
                     'w3': ['m3', 'm5', 'm2', 'm4', 'm1'], 
                     'w4': ['m1', 'm2', 'm5', 'm4', 'm3'], 
                     'w5': ['m3', 'm2', 'm5', 'm1', 'm4']}


matches = gale_shapley(men_preferences, women_preferences)
print(matches)

def gale_shapley_wrapper():
    # Vos données d'entrée
    men_preferences = {'m1': ['w3', 'w4', 'w5', 'w1', 'w2'], 
                       'm2': ['w3', 'w4', 'w2', 'w5', 'w1'], 
                       'm3': ['w3', 'w4', 'w1', 'w2', 'w5'], 
                       'm4': ['w5', 'w4', 'w2', 'w3', 'w1'], 
                       'm5': ['w3', 'w1', 'w4', 'w5', 'w2']}
    women_preferences = {'w1': ['m3', 'm2', 'm5', 'm1', 'm4'], 
                         'w2': ['m3', 'm1', 'm5', 'm4', 'm2'], 
                         'w3': ['m3', 'm5', 'm2', 'm4', 'm1'], 
                         'w4': ['m1', 'm2', 'm5', 'm4', 'm3'], 
                         'w5': ['m3', 'm2', 'm5', 'm1', 'm4']}
    
    # Appel de la fonction gale_shapley avec les données d'entrée
    gale_shapley(men_preferences, women_preferences)

# Mesurez le temps pris par la fonction gale_shapley
execution_time = timeit.timeit(gale_shapley_wrapper, number=1)

print("Execution time:", execution_time, "seconds")