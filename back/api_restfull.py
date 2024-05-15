from flask import Flask, jsonify, request
from flask_cors import CORS
from collections import Counter
import sqlite3
from sqlite_utils import Database
import os

# SI ERREUR VOICI LA COMMANDE : py -m pip install scikit-learn==1.2.2
api_key = 'a1b1045de421855d4d44bb2b53d4da8f'

app = Flask(__name__)
# Allow all link CORS
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
            cursor.execute("SELECT * FROM Hello")
            hello = cursor.fetchone()
            conn.close()

            return jsonify(hello[0])

        except sqlite3.Error as e:
            return jsonify({'error': str(e)}), 500

    else:
        return jsonify({'error': "nul"}), 50


@app.route('/api/gale_shapley', methods=['POST'])
def gale_shapley_route():
    data = request.json
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

                proposals[(man, best_choice)] = (
                    women_preferences[best_choice].index(man), men_preferences[man].index(best_choice))
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
def create_group():
    """
    Methods that creates a new group and update the student group (for the session)
    Example of data and post request to call in the front : 
    const data = {
          "students_id":[1,2]
        };
        const jsonData = JSON.stringify(data);

        const response = await axios.post("http://127.0.0.1:5000/api/create_group", jsonData, {
          headers: {
            'Content-Type': 'application/json'
          }}
        );

    Returns:
    _type_: _description_
"""   
    print('Enter create group function')

    # Retrieve parameters from the request body
    studentsID = request.json['students_id']  # Students ids members of the group assuming the parameters are sent in JSON format

    # Il faut utiliser os.path.join pour que ce soit multiplateforme
    db = os.path.join(os.getcwd(), 'db', 'parcoursup.sqlite')
    if os.path.exists(db):
        conn = sqlite3.connect(db)
        cursor = conn.cursor()

        try:
            # Create the group in the table GROUPE and return the ID
            sqlRequest = cursor.execute("INSERT INTO GROUPE VALUES (NULL, NULL, NULL, NULL) RETURNING ID")
            groupID = sqlRequest.fetchone()
            
            # Insert in ETUDIANT_GROUPE table with the group ID
            queryParameters = [(id, groupID[0]) for id in studentsID]
            
            cursor.executemany("INSERT INTO ETUDIANT_GROUPE VALUES (?, ?)", queryParameters)
            res = cursor.fetchone()  # Fetch all rows from the result set
 
            # Commit the insertions
            conn.commit()
            conn.close()

            # Convert data to JSON format
            return jsonify({'result': groupID}), 200

        except sqlite3.Error as e:
            print(e)
            return jsonify({'error': str(e)}), 500   
    else:
        return jsonify({'error': "nul"}), 50


@app.route('/api/create_students', methods=['POST'])
def create_students():
    """
    Add all the students data from the csv file.
    Called right after the csv file of student is read.
    :return:
    """
    print('Enter create students function')

    # Retrieve parameters from the request body
    sessionID = request.json.get('sessionID')  # assuming the parameters are sent in JSON format
    students = request.json.get('data')

    db = os.path.join(os.getcwd(), 'db', 'parcoursup.sqlite')
    if os.path.exists(db):
        conn = sqlite3.connect(db)
        cursor = conn.cursor()

        try:
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='ETUDIANT';")
            table_exists = cursor.fetchone() is not None

            if table_exists:
                cursor.execute(f"DELETE FROM ETUDIANT WHERE FK_Session ='{sessionID}'")

            # Insert student data (without RETURNING)
            queryParameters = [(data['Nom'], data['Prenom'], data['Email'], sessionID) for data in students]

            cursor.executemany(
                "INSERT INTO ETUDIANT (Nom, Prenom, Email, FK_Session) VALUES (?, ?, ?, ?)",
                queryParameters
            )

            # Commit the insertions
            conn.commit()
            conn.close()

            response = {
                "result": "Done"
            }
            return jsonify(response), 200

        except sqlite3.Error as e:
            return jsonify({'error': str(e)}), 500
    else:
        return jsonify({'error': "can't find database"}), 50
            
            
@app.route('/api/create_session', methods=['POST'])
def create_session():
    """
_summary_
Method that create a session, take in parameter a name, 
the group and project deadline, and the fk user creator
Example of data and post request to call in the front : 
    const data = {
       "session":["TestProjetTIC","14/05/2024", "25/05/2024", 5, 6 1]
     };
     const jsonData = JSON.stringify(data);

Returns:
    _type_: _description_
"""   
    print('Enter create session function')
    # Retrieve parameters from the request body
    session = request.json.get('session') # json item

    # Il faut utiliser os.path.join pour que ce soit multiplateforme
    db = os.path.join(os.getcwd(), 'db', 'parcoursup.sqlite') 
    if os.path.exists(db):
        conn = sqlite3.connect(db)
        cursor = conn.cursor()
        try:
            # Create the group in the table GROUPE and return the ID
            sessionName = session[0]
            sessionDeadlineGroup = session[1]
            sessionDeadlineProjet = session[2]
            sessionNbEtudiantMin = session[3]
            sessionNbEtudiantMax = session[4]
            sessionFKUtilisateur = session[5]
            sessionData = [sessionName, sessionDeadlineGroup, sessionDeadlineProjet, sessionNbEtudiantMin, sessionNbEtudiantMax, sessionFKUtilisateur]
             
            sqlRequest = cursor.execute("INSERT INTO SESSION VALUES (NULL, ?, ?, ?, ?, ?, ?) RETURNING ID", sessionData)
            sessionID = sqlRequest.fetchone()

            # Commit the insertions
            conn.commit()
            conn.close()

            # Convert data to JSON format
            return jsonify({'result': sessionID}), 200

        except sqlite3.Error as e:
            return jsonify({'error': str(e)}), 500   
    else:
        return jsonify({'error': "nul"}), 50
       
@app.route('/api/delete_session', methods=['POST'])
def delete_session():
    """
_summary_
Method that delete a session, take in parameter the id.
Returns:
    _type_: _description_
"""   
    print('Enter delete session function')
    # Retrieve parameters from the request body
    sessionID = request.json.get('sessionID') # json item

    # Il faut utiliser os.path.join pour que ce soit multiplateforme
    db = os.path.join(os.getcwd(), 'db', 'parcoursup.sqlite') 
    if os.path.exists(db):
        conn = sqlite3.connect(db)
        cursor = conn.cursor()
        try:           
            sqlRequest = cursor.execute("DELETE FROM SESSION WHERE ID = ?;", (sessionID,))
            res = sqlRequest.fetchone()
            print("Delete Session " + str(sessionID) + " : OK")

            # Commit the delete
            conn.commit()
            conn.close()
            
            # Convert data to JSON format
            return jsonify({'result': res}), 200

        except sqlite3.Error as e:
            return jsonify({'error': str(e)}), 500   
    else:
        return jsonify({'error': "nul"}), 50


if __name__ == '__main__':
    app.run(debug=True)
