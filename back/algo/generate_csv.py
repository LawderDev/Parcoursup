import csv
import random
import string

def generate_csv(filename, num_rows):
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=';')

        writer.writerow(['Nom', 'Prenom', 'Email'])

        for i in range(num_rows):
            last_name = ''.join(random.choice(string.ascii_uppercase) for ln in range(5))
            first_name = ''.join(random.choice(string.ascii_lowercase) for fn in range(5))

            email = f"{first_name}.{last_name}@etu-u.bordeaux.fr"

            print(last_name, first_name, email)
            writer.writerow([last_name, first_name, email])

if __name__ == '__main__':
    filename = 'name_file.csv'
    num_rows = 50

    generate_csv(filename, num_rows)
    print(f"CSV file generated: {filename}")
