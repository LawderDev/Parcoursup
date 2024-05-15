import csv
import io
import random
import string
import json


def generate_csv_file(filename, num_rows):
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


def csv_file_reader(csv_file, json_file):
    """
    Read CSV file and convert it into a JSON file.

    Args:
      csv_file (str): name csv file.
      json_file (str): name JSON file.

    Retours:
      json
    """

    donnees_json = []

    with open(csv_file, 'r') as csv_file, open(json_file, 'w') as json_file:
        for num, ligne in enumerate(csv_file):
            if num > 1:
                colonnes = ligne.strip().split(';')

                if len(colonnes) != 3:
                    continue

                donnee = {
                    "Nom": colonnes[0],
                    "Prenom": colonnes[1],
                    "Email": colonnes[2]
                }

                # Ajout du dictionnaire à la liste
                donnees_json.append(donnee)

            json.dump(donnees_json, json_file, indent=4)
        return donnees_json

def generate_csv(num_rows):
    csv_string = io.StringIO()
    writer = csv.writer(csv_string, delimiter=';')

    writer.writerow(['Nom', 'Prenom', 'Email'])

    for i in range(num_rows):
        last_name = ''.join(random.choice(string.ascii_uppercase) for _ in range(5))
        first_name = ''.join(random.choice(string.ascii_lowercase) for _ in range(5))
        email = f"{first_name}.{last_name}@etu-u.bordeaux.fr"

        writer.writerow([last_name, first_name, email])

    return csv_string.getvalue()

def csv_to_json(csv_data_string, json_file):
  """Converts CSV data (string or file) to JSON format and saves it to a file.

  Args:
      csv_data_string (str or file): CSV data in string or file format.
      json_file (str): Path to the output JSON file.
  """

  if isinstance(csv_data_string, str):
    # Read CSV data from string
    csv_data = csv_data_string.splitlines()
  else:
    # Read CSV data from file
    print(type(csv_data_string))
    with open(csv_data_string, 'r') as csv_file:
      csv_data = csv_file.readlines()

  # Skip header row
  csv_data = csv_data[1:]

  # Convert CSV data to JSON format
  data_json = []
  for row in csv_data:
    columns = row.strip().split(';')
    data = {
      "Nom": columns[0],
      "Prenom": columns[1],
      "Email": columns[2]
    }
    data_json.append(data)

  # Write JSON data to file
  #with open(json_file, 'w') as json_file:
  #  json.dump(data_json, json_file, indent=4)

  return data_json
