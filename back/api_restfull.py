from flask import Flask, jsonify, request
from flask_cors import CORS
from collections import Counter
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

@app.route('/api/gale_shapley', methods=['POST'])
def gale_shapley_route():
    data = request.json["data"]
    if 'men_preferences' in data and 'women_preferences' in data:
        men_preferences = data['men_preferences']
        women_preferences = data['women_preferences']
        res = gale_shapley(women_preferences, men_preferences)
        return jsonify(result=res)
    else:
        return jsonify({'error': 'Invalid request'}), 400

def gale_shapley(women_preferences, men_preferences):
    waiting_list = []
    proposals = {}
    count = 0
    women_available = {man: list(women_preferences.keys()) for man in men_preferences.keys()}
    men_available = men_preferences.copy()

    while len(waiting_list) < len(men_preferences):
        for man in men_preferences.keys():
            if man not in waiting_list:
                women = men_available[man]
                best_choice = women[0]

                proposals[(man, best_choice)] = (women_preferences[best_choice].index(man), men_preferences[man].index(best_choice))
                del women_available[man][0]

        overlays = Counter([key[1] for key in proposals.keys()])
        for woman in overlays.keys():
            if overlays[woman] > 1:
                pairs_to_drop = sorted({pair: proposals[pair] for pair in proposals.keys()
                                        if woman in pair}.items(),
                                    key=lambda x: (x[1][1], x[1][0]))[1:]
                for p_to_drop in pairs_to_drop:
                    del proposals[p_to_drop[0]]
                    del men_available[p_to_drop[0][0]][0]

        waiting_list = [man[0] for man in proposals.keys()]
        count += 1

    matched_pairs = [{'man': pair[0], 'woman': pair[1]} for pair in proposals.keys()]
    return {'matched_pairs': matched_pairs}


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
    
@app.route('/api/student_is_in_group', methods=['POST'])
def is_in_group():
    """
_summary_
Method that delete a session, take in parameter the id.
Returns:
    _type_: _description_
"""   
    print('Enter student is in group function')
    # Retrieve parameters from the request body
    studentID = request.json.get('studentID')

    # Il faut utiliser os.path.join pour que ce soit multiplateforme
    db = os.path.join(os.getcwd(), 'db', 'parcoursup.sqlite') 
    if os.path.exists(db):
        conn = sqlite3.connect(db)
        cursor = conn.cursor()
        try:
            sqlRequest = cursor.execute("SELECT FK_Groupe from ETUDIANT_GROUPE WHERE FK_Etudiant = ?", (studentID,))
            res = sqlRequest.fetchone()
            
            conn.close()

            if res != None:
                res = True # Déjà dans un groupe
            else:
                res = False # Pas dans un groupe
                
            # Convert data to JSON format
            return jsonify({'result': res}), 200

        except sqlite3.Error as e:
            return jsonify({'error': str(e)}), 500   
    else:
        return jsonify({'error': "nul"}), 50

if __name__ == '__main__':
    app.run(debug=True)