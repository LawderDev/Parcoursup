from flask import Flask, jsonify, request
from flask_cors import CORS
from collections import Counter
import sqlite3
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


@app.route('/api/get_sessions', methods=['GET'])
def get_sessions():
    print('enter')
    # Il faut utiliser os.path.join pour que ce soit multiplateforme
    db = os.path.join(os.getcwd(), 'db', 'parcoursup.sqlite')
    if os.path.exists(db):
        conn = sqlite3.connect(db)
        cursor = conn.cursor()

        try:
            # Retrieve data from SQLite database

            cursor.execute("SELECT id, Nom, Deadline_Choix_Projet FROM SESSION")

            response = cursor.fetchall()
            print(response)

            sessions = []
            for idx,session in enumerate(response):
                session_dict = {
                    'id': response[idx][0],
                    'nom': response[idx][1],
                    'end_date': response[idx][2],
                }
                sessions.append(session_dict)

            conn.close()

            # Convert data to JSON format
            return jsonify(sessions)

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
    women_available = {man: list(women_preferences.keys())
                       for man in men_preferences.keys()}
    men_available = men_preferences.copy()

    while len(waiting_list) < len(men_preferences):
        for man in men_preferences.keys():
            if man not in waiting_list:
                women = men_available[man]
                best_choice = women[0]

                proposals[(man, best_choice)] = (women_preferences[best_choice].index(
                    man), men_preferences[man].index(best_choice))
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

    matched_pairs = [{'man': pair[0], 'woman': pair[1]}
                     for pair in proposals.keys()]
    return {'matched_pairs': matched_pairs}


@app.route('/api/create_group', methods=['POST'])
def create_group():
    """
    Methods that creates a new group and update the student group (for the session)

    Example of data and post request to call in the front :
            
        const data = { 
        "data" : [
            {'studentID': 1},
            {'studentID': 2}
        ]     
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
    studentsID = request.json.get('data')  # Students ids members of the group assuming the parameters are sent in JSON format
    
    # Il faut utiliser os.path.join pour que ce soit multiplateforme
    db = os.path.join(os.getcwd(), 'db', 'parcoursup.sqlite')

    if os.path.exists(db):
        conn = sqlite3.connect(db)
        cursor = conn.cursor()

        try:
            # Create the group in the table GROUPE and return the ID
            sqlRequest = cursor.execute(
                "INSERT INTO GROUPE VALUES (NULL, NULL, NULL, NULL) RETURNING ID")
            groupID = sqlRequest.fetchone()
            
            # Insert in ETUDIANT_GROUPE table with the group ID
            queryParameters = [(data['studentID'], groupID[0]) for data in studentsID]
            cursor.executemany("INSERT INTO ETUDIANT_GROUPE VALUES (?, ?)", queryParameters)
 
            # Commit the insertions
            conn.commit()
            conn.close()

            # Convert data to JSON format
            return jsonify({'result': groupID}), 200

        except sqlite3.Error as e:
            return jsonify({'error': str(e)}), 500   
    else:
        return jsonify({'error': "nul"}), 50


@app.route('/api/create_session', methods=['POST'])
def create_session():
    """
    _summary_
        Method that create a session, take in parameter a name,
        the group and project deadline, and the fk user creator

    Example of data and post request to call in the front :
    const data = { 
        "data" : [
            {'Nom': 1,
            'Deadline_Creation_Groupe':'12/02/2024', 
            'Deadline_Choix_Projet':'12/04/2024',
            'Nb_Etudiant_Min':4,
            'Nb_Etudiant_Max':5,
            'Etat':'Choosing',
            'Fk_Utilisateur':1,
            }
        ]     
        };
     const jsonData = JSON.stringify(data);

    Returns:
        _type_: _description_
    """
    print('Enter create session function')
    # Retrieve parameters from the request body
    session = request.json.get('data')
    
    # Il faut utiliser os.path.join pour que ce soit multiplateforme
    db = os.path.join(os.getcwd(), 'db', 'parcoursup.sqlite')
    print(db)
    if os.path.exists(db):
        conn = sqlite3.connect(db)
        cursor = conn.cursor()
        try:
            queryParameters = (session[0]['Nom'], session[0]['Deadline_Creation_Groupe'], session[0]['Deadline_Choix_Projet'], session[0]['Nb_Etudiant_Min'], session[0]['Nb_Etudiant_Max'], session[0]['Etat'], session[0]['FK_Utilisateur'])
             
            sqlRequest = cursor.execute("INSERT INTO SESSION VALUES (NULL, ?, ?, ?, ?, ?, ?, ?) RETURNING ID", queryParameters)
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
    
           
@app.route('/api/update_session', methods=['POST'])
def update_session():
    """
    _summary_
        Method that create a session, take in parameter a name,
        the group and project deadline, and the fk user creator

    Example of data and post request to call in the front :
    const data = { 
        "session_ID":1,
        "data" : [
            {
            'Nom': 1,
            'Deadline_Creation_Groupe':'12/02/2024', 
            'Deadline_Choix_Projet':'12/04/2024',
            'Nb_Etudiant_Min':4,
            'Nb_Etudiant_Max':5,
            'Etat':'Choosing',
            'Fk_Utilisateur':1,
            }
        ]     
        };
     const jsonData = JSON.stringify(data);

    Returns:
        _type_: _description_
    """
    print('Enter create session function')
    # Retrieve parameters from the request body
    sessionID = request.json.get('session_ID')
    session = request.json.get('data')
    
    # Il faut utiliser os.path.join pour que ce soit multiplateforme
    db = os.path.join(os.getcwd(), 'db', 'parcoursup.sqlite') 
    if os.path.exists(db):
        conn = sqlite3.connect(db)
        cursor = conn.cursor()
        try:
            queryParameters = [(session[0]['Nom'], session[0]['Deadline_Creation_Groupe'], session[0]['Deadline_Choix_Projet'], session[0]['Nb_Etudiant_Min'], session[0]['Nb_Etudiant_Max'], session[0]['Etat'], session[0]['FK_Utilisateur'], sessionID)]
             
            sqlRequest = cursor.execute("UPDATE SESSION SET Nom = ?, Deadline_Creation_Groupe = ?, Deadline_Choix_Projet = ?, Nb_Etudiant_Min = ?, Nb_Etudiant_Max = ?, Etat = ?, FK_Utilisateur = ? WHERE ID = ?", queryParameters[0])
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
    sessionID = request.json.get('sessionID')  # json item

    # Il faut utiliser os.path.join pour que ce soit multiplateforme
    db = os.path.join(os.getcwd(), 'db', 'parcoursup.sqlite')
    if os.path.exists(db):
        conn = sqlite3.connect(db)
        cursor = conn.cursor()
        try:           
            sqlRequest = cursor.execute("DELETE FROM SESSION WHERE ID = ?;", (sessionID,))
            res = sqlRequest.fetchone()

            # Commit the delete
            conn.commit()
            conn.close()
            
            # Convert data to JSON format
            return jsonify({'result': res}), 200

        except sqlite3.Error as e:
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

@app.route('/api/student_is_in_group', methods=['POST'])
def is_in_group():
    """
    _summary_
        Method that return if a student is in a group, take in parameter the student id.
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

@app.route('/api/create_project', methods=['POST'])
def create_project():
    """
    Methods that creates a new project
    Example of data and post request to call in the front : 
    const data = { 
        "data" : [
            {'Nom': 1,
            'Description':'desc',
            'Nb_Etudiant_Min':4,
            'Nb_Etudiant_Max':5,
            'FK_Session':1,
            }
        ]     
        };
        const jsonData = JSON.stringify(data);

        const response = await axios.post("http://127.0.0.1:5000/api/create_project", jsonData, {
          headers: {
            'Content-Type': 'application/json'
          }}
        );

    Returns:
    _type_: _description_
"""   
    print('Enter create project function')

    # Retrieve parameters from the request body
    projet = request.json.get('data')  # assuming the parameters are sent in JSON format

    # Il faut utiliser os.path.join pour que ce soit multiplateforme
    db = os.path.join(os.getcwd(), 'db', 'parcoursup.sqlite') 
    if os.path.exists(db):
        conn = sqlite3.connect(db)
        cursor = conn.cursor()

        try:
            # Create the group in the table GROUPE and return the ID
            queryParameters = [(projet[0]['Nom'], projet[0]['Description'], projet[0]['Nb_Etudiant_Min'], projet[0]['Nb_Etudiant_Max'], projet[0]['FK_Session'])]

            sqlRequest = cursor.execute("INSERT INTO PROJET VALUES (NULL, ?, ?, ?, ?, ?) RETURNING ID", queryParameters[0])
            projectID = sqlRequest.fetchone()
            
            # Commit the insertions
            conn.commit()
            conn.close()

            # Convert data to JSON format
            return jsonify({'result': projectID}), 200

        except sqlite3.Error as e:
            return jsonify({'error': str(e)}), 500   
    else:
        return jsonify({'error': "nul"}), 50

@app.route('/api/reaffect_group', methods=['POST'])
def reaffect_group():
    """
    Update all the students' groups if they have been changed by a user on the front-end.

    Example of data and post request to call in the front :
    const data = {
        "data": [
            {
              "id_student": 1,
              "id_new_group": 56
            },
            {
              "id_student": 2,
              "id_new_group": 4
            }
        ]
    }

    const jsonData = JSON.stringify(data);

        const response = await axios.post("http://127.0.0.1:5000/api/reaffect_group", jsonData, {
          headers: {
            'Content-Type': 'application/json'
          }}
        );

    :return:
    """
    print('Enter reaffect group function')

    # Retrieve parameters from the request body
    group = request.json.get('data')

    db = os.path.join(os.getcwd(), 'db', 'parcoursup.sqlite')
    if os.path.exists(db):
        conn = sqlite3.connect(db)
        cursor = conn.cursor()

        try:
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='ETUDIANT-GROUPE';")

            queryParameters = [(student['id_new_group'], student['id_student']) for student in group]

            cursor.executemany(
                "UPDATE ETUDIANT_GROUPE SET FK_Groupe=? WHERE FK_ETUDIANT=?",
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
            print(e)
            return jsonify({'error': str(e)}), 500
    else:
        return jsonify({'error': "can't find database"}), 50
      
@app.route('/api/delete_project', methods=['POST'])
def delete_project():
    """
    _summary_
    Method that delete a project, take in parameter the id.
    Returns:
        _type_: _description_
    """
    print('Enter delete project function')
    # Retrieve parameters from the request body
    projectID = request.json.get('projectID') # json item

    # Il faut utiliser os.path.join pour que ce soit multiplateforme
    db = os.path.join(os.getcwd(), 'db', 'parcoursup.sqlite') 
    if os.path.exists(db):
        conn = sqlite3.connect(db)
        cursor = conn.cursor()
        try:           
            sqlRequest = cursor.execute("DELETE FROM PROJET WHERE ID = ?;", (projectID,))
            res = sqlRequest.fetchone()

            # Commit the delete
            conn.commit()
            conn.close()
            
            # Convert data to JSON format
            return jsonify({'result': res}), 200

        except sqlite3.Error as e:
            return jsonify({'error': str(e)}), 500   
    else:
        return jsonify({'error': "nul"}), 50


@app.route('/api/get_all_projects', methods=['POST'])
def get_all_projects():
    """
    _summary_
    Method that retrieve all the projects from a session.
        const data = {
            "sessionID" : 1
        };
        const jsonData = JSON.stringify(data);

        const response = await axios.post("http://127.0.0.1:5000/api/get_all_projects", jsonData, {
          headers: {
            'Content-Type': 'application/json'
          }}
        );
    Returns:
    Json with all the projects from a session
"""
    print('Enter get all projects function')

    # Retrieve parameters from the request body
    sessionID = request.json.get('sessionID')

    db = os.path.join(os.getcwd(), 'db', 'parcoursup.sqlite')
    if os.path.exists(db):
        conn = sqlite3.connect(db)
        cursor = conn.cursor()

        try:
            # Retrieve data from SQLite database
            cursor.execute("SELECT * FROM Projet WHERE FK_Session = ? ;", (sessionID,))
            response = cursor.fetchall()

            #Prepare data for the front-end
            projects = []
            for idx, project in enumerate(response):
                project_dict = {
                    'id': response[idx][0],
                    'nom': response[idx][1],
                    'description': response[idx][2],
                    'min_etu': response[idx][3],
                    'max_etu': response[idx][4],
                    'id_session': response[idx][5]
                }
                projects.append(project_dict)

            print(projects)

            conn.close()

            # Convert data to JSON format
            return jsonify(projects)

        except sqlite3.Error as e:
            return jsonify({'error': str(e)}), 500
    else:
        return jsonify({'error': "nul"}), 50

@app.route('/api/update_project', methods=['POST'])
def update_project():
    """
    Update the project in the database after being changed on the front-end.

    Example of data and post request to call in the front :
    const data = {
        "data": [
            {
                'id': 1,
                'nom': 'Parcoursup',
                'description': 'Projet parcoursup',
                'min_etu': 6,
                'max_etu': 7,
                'id_session': 1
            }
        ]
    }

    const jsonData = JSON.stringify(data);

        const response = await axios.post("http://127.0.0.1:5000/api/update_project", jsonData, {
          headers: {
            'Content-Type': 'application/json'
          }}
        );

    :return:
    """
    print('Enter update project function')

    # Retrieve parameters from the request body
    data = request.json.get('data')[0]
    print(data)

    db = os.path.join(os.getcwd(), 'db', 'parcoursup.sqlite')
    if os.path.exists(db):
        conn = sqlite3.connect(db)
        cursor = conn.cursor()

        try:
            queryParameters = [data['nom'],
                                data['description'],
                                data['min_etu'],
                                data['max_etu'],
                                data['id'],
                                data['id_session']
                                ]

            sqlRequest = cursor.execute(
                "UPDATE PROJET SET Nom = ?, Description = ?, Nb_Etudiant_Min = ?, Nb_Etudiant_Max = ? WHERE ID = ? "
                "and FK_Session = ?;",
                queryParameters)
            res = sqlRequest.fetchone()

            # Commit the insertions
            conn.commit()
            conn.close()

            # Convert data to JSON format
            return jsonify({'result': res}), 200

        except sqlite3.Error as e:
            print(e)
            return jsonify({'error': str(e)}), 500
    else:
        return jsonify({'error': "can't find database"}), 50

@app.route('/api/affect_preference_groupe', methods=['POST'])
def affect_preference_groupe():
    """
    Methods that insert a group project's preference
    Example of data and post request to call in the front : 
    const data = {
        "data": [
            {
              "groupID": 1,
              "projectID": 1,
              "order": 1
            },
            {
              "groupID": 1,
              "projectID": 2,
              "order": 2
            }
        ]
    }
        const jsonData = JSON.stringify(data);

    Returns:
    _type_: _description_
"""   
    print('Enter affect preference group function')

    # Retrieve parameters from the request body
    preferences = request.json.get('data')  # assuming the parameters are sent in JSON format

    # Il faut utiliser os.path.join pour que ce soit multiplateforme
    db = os.path.join(os.getcwd(), 'db', 'parcoursup.sqlite') 
    if os.path.exists(db):
        conn = sqlite3.connect(db)
        cursor = conn.cursor()

        try:
            for preference in preferences:
                group_id, project_id, order = preference['groupID'], preference['projectID'], preference['order']

                # Check for existing entry with projectID and groupID
                existing_row = cursor.execute("SELECT * FROM PREFERENCE_GROUPE WHERE FK_Projet = ? AND FK_Groupe = ?", (project_id, group_id)).fetchone()

                if existing_row:
                    # Update existing order
                    cursor.execute("UPDATE PREFERENCE_GROUPE SET Ordre_Preference = ? WHERE FK_Projet = ? AND FK_Groupe = ?",
                                   (order, project_id, group_id))
                else:
                    # Insert new preference
                    cursor.execute("INSERT INTO PREFERENCE_GROUPE (FK_Groupe, FK_Projet, Ordre_Preference) VALUES (?, ?, ?)",(group_id, project_id, order))

                conn.commit()
            conn.close()

            # Convert data to JSON format
            return jsonify({'result': "done"}), 200

        except sqlite3.Error as e:
            print(e)
            return jsonify({'error': str(e)}), 500   
    else:
        return jsonify({'error': "nul"}), 50


@app.route('/api/affect_preference_projet', methods=['POST'])
def affect_preference_projet():
    """
    Methods that insert a group project's preference
    Example of data and post request to call in the front :
    const data = {
        "data": [
            {
              "projectID": 1,
              "groupID": 1,
              "order": 1
            },
            {
              "projectID": 1,
              "groupID": 2,
              "order": 2
            }
        ]
    }
        const jsonData = JSON.stringify(data);

    Returns:
    _type_: _description_
"""
    print('Enter affect preference project function')

    # Retrieve parameters from the request body
    preferences = request.json.get('data')  # assuming the parameters are sent in JSON format

    # Il faut utiliser os.path.join pour que ce soit multiplateforme
    db = os.path.join(os.getcwd(), 'db', 'parcoursup.sqlite')
    if os.path.exists(db):
        conn = sqlite3.connect(db)
        cursor = conn.cursor()

        try:
            for preference in preferences:
                project_id, group_id, order = preference['projectID'], preference['groupID'], preference['order']

                # Check for existing entry with projectID and groupID
                cursor.execute("SELECT * FROM PREFERENCE_PROJET WHERE FK_Projet = ? AND FK_Groupe = ?", (project_id, group_id))
                existing_row = cursor.fetchone()

                if existing_row:
                    # Update existing order
                    cursor.execute("UPDATE PREFERENCE_PROJET SET Ordre_Preference = ? WHERE FK_Projet = ? AND FK_Groupe = ?",
                                   (order, project_id, group_id))
                else:
                    # Insert new preference
                    cursor.execute("INSERT INTO PREFERENCE_PROJET (FK_Projet, FK_Groupe, Ordre_Preference) VALUES (?, ?, ?)",
                                   (project_id, group_id,  order))

                conn.commit()
            conn.close()

            # Convert data to JSON format
            return jsonify({'result': "done"}), 200

        except sqlite3.Error as e:
            print(e)
            return jsonify({'error': str(e)}), 500
    else:
        return jsonify({'error': "nul"}), 50

if __name__ == '__main__':
    app.run(debug=True)
