import csv
import random
import string
import json


def generate_csv(filename, num_rows):
    """
    Function that generates fake CSV to test
    :param filename:
    :param num_rows:
    :return:
    """
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=';')

        writer.writerow(['Nom', 'Prenom', 'Email'])

        for i in range(num_rows):
            last_name = ''.join(random.choice(string.ascii_uppercase) for ln in range(5))
            first_name = ''.join(random.choice(string.ascii_lowercase) for fn in range(5))

            email = f"{first_name}.{last_name}@etu-u.bordeaux.fr"

            print(last_name, first_name, email)
            writer.writerow([last_name, first_name, email])


def csv_read(csv_file, json_file):
    """
    Read CSV file and convert it into a JSON file.

    Args:
      csv_file (str): name csv file.
      json_file (str): name JSON file.

    Retours:
      json
    """

    donnees_json = []

    id_compteur = 1

    with open(csv_file, 'r') as csv_file, open(json_file, 'w') as json_file:
        for num, ligne in enumerate(csv_file):
            if num > 1:
                colonnes = ligne.strip().split(';')

                if len(colonnes) != 3:
                    continue

                donnee = {
                    "id": id_compteur,
                    "Nom": colonnes[0],
                    "Prenom": colonnes[1],
                    "Email": colonnes[2]
                }

                # Ajout du dictionnaire à la liste
                donnees_json.append(donnee)

                id_compteur += 1

            json.dump(donnees_json, json_file, indent=4)
        return donnees_json
