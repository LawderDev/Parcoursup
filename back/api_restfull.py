from flask import Flask, jsonify
from flask_cors import CORS
import sqlite3
import os

#SI ERREUR VOICI LA COMMANDE : py -m pip install scikit-learn==1.2.2 
api_key = 'a1b1045de421855d4d44bb2b53d4da8f'

app = Flask(__name__)
#Allow all link CORS
CORS(app, resources={r"/api/*": {"origins": "*"}})


@app.route('/api/hello_world', methods=['GET'])
def get_hello_world():
    print('enter')
    # Il faut utiliser os.path.join pour que ce soit multiplateforme
    db = os.path.join(os.getcwd(), 'db', 'parcoursup.sqlite') 
    print(db)
    if os.path.exists(db):
        conn = sqlite3.connect(db)
        cursor = conn.cursor()

        try:
            # Retrieve data from SQLite database
          
            cursor.execute("SELECT * FROM Hello")
 
            hello = cursor.fetchone()

            conn.close()

            # Convert data to JSON format
            return jsonify(hello[0])

        except sqlite3.Error as e:
            return jsonify({'error': str(e)}), 500
        
    else:
        return jsonify({'error': "nul"}), 50
    
@app.route('/api/create_group', methods=['GET'])
def create_group():
    print('Enter create group function')
    # Il faut utiliser os.path.join pour que ce soit multiplateforme
    db = os.path.join(os.getcwd(), 'db', 'parcoursup.sqlite') 
    if os.path.exists(db):
        conn = sqlite3.connect(db)
        cursor = conn.cursor()

        try:
            # Create the group in the table GROUPE and return the ID
            request = cursor.execute("INSERT INTO GROUPE VALUES (NULL, NULL, NULL, NULL) RETURNING ID")
            res = request.fetchone()
            
            # Update ETUDIANT table with the group ID for this SESSION
            rows = [
                ("TEMP",),
                ("TEST",),
            ]
            request = cursor.executemany("UPDATE ETUDIANT SET FK_Groupe = 25 WHERE Email = ? and FK_Session = 1", rows)
            res = request.fetchall()
            
            # Commit the insertions
            conn.commit()
            conn.close()

            # Convert data to JSON format
            return jsonify(res)

        except sqlite3.Error as e:
            return jsonify({'error': str(e)}), 500   
    else:
        return jsonify({'error': "nul"}), 50


if __name__ == '__main__':
    app.run(debug=True)