from flask import Flask, jsonify, request
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
    
@app.route('/api/create_group', methods=['POST'])
# Example of data and post request to call in the front : 
# const data = {
#       "sessionID":1,
#       "emails":["Benjamin.Bancal@etu.u-bordeaux.fr","Sandra.Ly@etu.u-bordeaux.fr"]
#     };
#     const jsonData = JSON.stringify(data);

#     const response = await axios.post("http://127.0.0.1:5000/api/create_group", jsonData, {
#       headers: {
#         'Content-Type': 'application/json'
#       }}
#     );
def create_group():
    print('Enter create group function')
    
    # Retrieve parameters from the request body
    sessionID = request.json.get('sessionID')  # assuming the parameters are sent in JSON format
    studentEmails = request.json.get('emails')
    
    # Il faut utiliser os.path.join pour que ce soit multiplateforme
    db = os.path.join(os.getcwd(), 'db', 'parcoursup.sqlite') 
    if os.path.exists(db):
        conn = sqlite3.connect(db)
        cursor = conn.cursor()

        try:
            # Create the group in the table GROUPE and return the ID
            sqlRequest = cursor.execute("INSERT INTO GROUPE VALUES (NULL, NULL, NULL, NULL) RETURNING ID")
            groupID = sqlRequest.fetchone()
            
            # Update ETUDIANT table with the group ID for this SESSION
            queryParameters = [(groupID[0], email, sessionID) for email in studentEmails]
            
            sqlRequest = cursor.executemany("UPDATE ETUDIANT SET FK_Groupe = ? WHERE Email = ? and FK_Session = ?", queryParameters)
            res = sqlRequest.fetchone()
            
            # Commit the insertions
            conn.commit()
            conn.close()

            # Convert data to JSON format
            return jsonify({'result': "done"}), 200

        except sqlite3.Error as e:
            return jsonify({'error': str(e)}), 500   
    else:
        return jsonify({'error': "nul"}), 50


if __name__ == '__main__':
    app.run(debug=True)