import random

# Cette fonction est complètement random, ce qui veut dire qu'un homme ou une femme peut ne pas classer tous les autres hommes ou femmes (ce qui est fort probable dans le cas d'un parcoursup)
def generate_preferences(num_people):
    men_preferences = {}
    women_preferences = {}

    for i in range(1, num_people + 1):
        man = f"m{i}"
        woman = f"w{i}"
        other_women = [f"w{j}" for j in random.sample(range(1, num_people + 1), num_people - 1) if j != i]
        other_men = [f"m{j}" for j in random.sample(range(1, num_people + 1), num_people - 1) if j != i]

        men_preferences[man] = other_women
        women_preferences[woman] = other_men

    return men_preferences, women_preferences

# Usage:
num_people = 5
men_preferences, women_preferences = generate_preferences(num_people)
print("Men's preferences:", men_preferences)
print("Women's preferences:", women_preferences)

# On peut adapter pour que chaque homme classe chaque femme et inversement
def generate_preferences_full(num_people):
    men_preferences = {}
    women_preferences = {}

    all_people = [f"m{i}" for i in range(1, num_people + 1)] + [f"w{i}" for i in range(1, num_people + 1)]

    for person in all_people:
        if person.startswith("m"):
            preferences = [woman for woman in all_people if woman.startswith("w") and woman != person]
            random.shuffle(preferences)
            men_preferences[person] = preferences
        elif person.startswith("w"):
            preferences = [man for man in all_people if man.startswith("m") and man != person]
            random.shuffle(preferences)
            women_preferences[person] = preferences

    return men_preferences, women_preferences

# Usage
num_people = 5
men_preferences, women_preferences = generate_preferences_full(num_people)
print("Men's preferences:", men_preferences)
print("Women's preferences:", women_preferences)
