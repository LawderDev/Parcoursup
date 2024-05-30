import json

from dotenv import load_dotenv
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import CORS
from collections import Counter
from mailersend import emails
from flask_mail import Mail
import sqlite3
import os

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(os.getcwd(), 'db', 'parcoursup.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['MAIL_SERVER'] = os.getenv("MAIL_SERVER")
app.config['MAIL_PORT'] = os.getenv("MAIL_PORT")
app.config['MAIL_USERNAME'] = os.getenv("MAIL_USERNAME")
app.config['MAIL_PASSWORD'] = os.getenv("MAIL_PASSWORD")
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
mail = Mail(app)

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
CORS(app, supports_credentials=True, resources={r"/api/*": {"origins": "*"}})  # Allow CORS for all routes


class Utilisateur(db.Model):
    ID = db.Column(db.Integer, primary_key=True)
    Nom = db.Column(db.String(100), nullable=False)
    Prenom = db.Column(db.String(100), nullable=False)
    Email = db.Column(db.String(120), unique=True, nullable=False)
    Password = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"Utilisateur('{self.Nom}', '{self.Email}')"

    def is_active(self):
        return True

    def is_authenticated(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.ID)


@login_manager.user_loader
def load_user(user_id):
    try:
        return db.session.get(Utilisateur, int(user_id))
    except Exception as e:
        print(e)
        return None


@app.route('/api/register', methods=['POST'])
def register():
    """_summary_
        const data = { 
                "data" : [
                    {'Nom': "Test",
                    'Prenom': "test",
                    'Email':'test@test16.com', 
                    'Password':'monMDP'
                    }
                ]     
                };
            const jsonData = JSON.stringify(data);
            
        // User registration
        axiosInstance.post('/api/register',jsonData, {
          headers: {
            'Content-Type': 'application/json'
          }}
    Returns:
        _type_: _description_
    """
    try:
        print("enter register function")
        data = request.json.get('data')

        existing_user = Utilisateur.query.filter_by(Email=data[0]['Email']).first()
        if existing_user:
            return jsonify({'message': 'Email already exists'}), 400

        password = data[0]['Password']
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256', salt_length=16)

        new_user = Utilisateur(Nom=data[0]['Nom'], Prenom=data[0]['Prenom'], Email=data[0]['Email'],
                               Password=hashed_password)

        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'User created successfully'}), 201

    except Exception as e:
        print(e)
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@app.route('/api/login', methods=['POST'])
def login():
    """_summary_
        const data = { 
            "data" : [
                {
                'Email':'test@test16.com', 
                'Password':'monMDP'
                }
            ]     
            };
        const jsonData = JSON.stringify(data);

      // User login
      axiosInstance.post('/api/login',jsonData, {
          headers: {
            'Content-Type': 'application/json'
          }}).then(response => {
        console.log(response.data);
        
    Returns:
        _type_: _description_
    """
    try:
        print("enter login function")
        data = request.json.get('data')
        user = Utilisateur.query.filter_by(Email=data[0]['Email']).first()

        if not data or 'Email' not in data[0] or 'Password' not in data[0]:
            return jsonify({'message': 'Invalid request data'}), 400

        user = Utilisateur.query.filter_by(Email=data[0]['Email']).first()

        if user is None:
            return jsonify({'message': 'Invalid login'}), 401

        if user.Password is None or data[0]['Password'] is None:
            return jsonify({'message': 'Invalid password'}), 401

        if check_password_hash(user.Password, data[0]['Password']):
            login_user(user)
            return jsonify({'message': 'Logged in successfully'}), 200
        else:
            return jsonify({'message': 'Invalid password'}), 401
    except Exception as e:
        print(e)
        return jsonify({'error': str(e)}), 500

@app.route('/api/logout', methods=['GET'])
@login_required
def logout():
    try:
        logout_user()
        return jsonify({'message': 'Logged out successfully'}), 200
    except Exception as e:
        print(e)
        return jsonify({'error': str(e)}), 500


@app.route('/api/current_user', methods=['GET'])
@login_required
def get_current_user():
    """
        const jsonData = JSON.stringify(data);
    // Access protected route after login
        axiosInstance.get('/api/current_user')
      
    Returns:
        _type_: _description_
    """
    try:
        print("enter current user function")
        user = {
            'Nom': current_user.Nom,
            'Prenom' : current_user.Prenom,
            'Email': current_user.Email
        }
        return jsonify(user), 200
    except Exception as e:
        print(e)
        return jsonify({'error': str(e)}), 500


@app.route('/api/update_password', methods=['POST'])
@login_required
def update_password():
    """_summary_
    const data = { 
            "data" : [
                {
                'current_password':'monMDP', 
                'new_password':'monMDP2'
                }
            ]     
            };
        const jsonData = JSON.stringify(data);
    Returns:
        _type_: _description_
    """
    try:
        data = request.json.get('data')
        current_password = data['current_password']
        new_password = data['new_password']
        
        # Verify the current password
        if not check_password_hash(current_user.Password, current_password):
            return jsonify({'message': 'Current password is incorrect'}), 400
        
        # Update to the new password
        hashed_new_password = generate_password_hash(new_password, method='pbkdf2:sha256', salt_length=16)
        current_user.Password = hashed_new_password
        db.session.commit()
        return jsonify({'message': 'Password updated successfully'}), 200
    except Exception as e:
        print(e)
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
    
@app.route('/api/get_users', methods=['GET'])
def get_users():
    print('enter get users function')
    db = os.path.join(os.getcwd(), 'db', 'parcoursup.sqlite')
    if os.path.exists(db):
        try:
            
            conn = sqlite3.connect(db)
            cursor = conn.cursor()

            cursor.execute("SELECT * from UTILISATEUR")

            response = cursor.fetchall()

            users = []
            for user in response:
                user_dict = {
                    'id': user[0],
                    'name': user[1],
                    'firstname': user[2],
                    'email': user[3],
                    'password': user[4]
                }
                users.append(user_dict)

            conn.close()

            # Convert data to JSON format
            return jsonify(users)

        except sqlite3.Error as e:
            return jsonify({'error': str(e)}), 500
    else:
        return jsonify({'error': "nul"}), 50
    
@app.route('/api/delete_user', methods=['POST'])
def delete_user():
    """
    _summary_
        Method that delete a user, take in parameter the id.
    Returns:
        _type_: _description_
    """
    print('Enter delete user function')
    # Retrieve parameters from the request body
    userID = request.json.get('userID')  # json item

    # Il faut utiliser os.path.join pour que ce soit multiplateforme
    db = os.path.join(os.getcwd(), 'db', 'parcoursup.sqlite')
    if os.path.exists(db):
        conn = sqlite3.connect(db)
        cursor = conn.cursor()
        try:
            sqlRequest = cursor.execute("DELETE FROM UTILISATEUR WHERE ID = ?;", (userID,))
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
    
@app.route('/api/update_user', methods=['POST'])
def update_user():
    print('Enter update user function')
    # Retrieve parameters from the request body
    user = request.json.get('data')

    # Il faut utiliser os.path.join pour que ce soit multiplateforme
    db = os.path.join(os.getcwd(), 'db', 'parcoursup.sqlite')
    if os.path.exists(db):
        conn = sqlite3.connect(db)
        cursor = conn.cursor()
        try:
            
            queryParameters = [(user[0]['Nom'], user[0]['Prenom'], user[0]['Email'], user[0]['Password'],
                                user[0]['Id'])]

            sqlRequest = cursor.execute(
                "UPDATE UTILISATEUR SET Nom = ?, Prenom = ?, Email = ?, Password = ? WHERE ID = ?",
                queryParameters[0])
            userID = sqlRequest.fetchone()

            # Commit the insertions
            conn.commit()
            conn.close()

            # Convert data to JSON format
            return jsonify({'result': userID}), 200

        except sqlite3.Error as e:
            return jsonify({'error': str(e)}), 500
    else:
        return jsonify({'error': "nul"}), 50


# Initialize the database (run once to create the database)
# with app.app_context():
#     db.create_all()

###
# MAIL
###
@app.route('/api/send_mail_group', methods=['POST'])
def send_mail_group():
    """
    data = {
        "sessionID": 1
    };
    :return:
    """
    api_key = os.getenv("MAIL_API_KEY")
    mailer = emails.NewEmail(api_key)

    session_dict = get_session_data(session=request.json.get("sessionID"))
    students = get_all_groups_students(session=request.json.get("sessionID"))

    mail_list = []

    for group in students.values():
        mail_list.append(send_mail_simple_group(session_dict, group['id'], group['students']))

    # Send mail
    response = mailer.send_bulk(mail_list)
    objects = response.split("\n")
    if len(objects) < 2:
        for obj in objects:
            data = json.loads(obj)
        status = objects[0]
        message = data["message"]
        bulk_email_id = data["bulk_email_id"]

        response = {
            "status": status,
            "message": message,
            "bulk_email_id": bulk_email_id,
            "bulk_email_status": mailer.get_bulk_status_by_id(bulk_email_id)
        }

        if status == 202:
            return jsonify({"result": response}), 200
        else:
            return jsonify({"error": response}), 500
    else:
        return jsonify({"error": response}), 500


def send_mail_simple_group(session_dict, id_group, students):
    """
    Create and send the group mail to all the person of the group
    :param session_dict: dict containing all the information of the session
    :param id_group: id of the group
    :param students: dict with all the student of the group
    :return:
    """
    # -- Replacing values using the template

    nom_session = "{{nom_session}}"  # session_dict['name_session']
    list_etu = "{{list_etu}}"
    date_limit = "{{date_limit}}"  # session_dict['end_date_session']
    lien_choix_projet_template = "{{lien_choix_projet}}"  # session_dict['id']

    lien_choix_projet_groupe = os.getenv("SERVER_LINK") + '/' + str(session_dict['id']) + '/' + str(id_group)

    string_students = ""
    string_students_text = ""
    for i, student in enumerate(students):
        string_students += f"{student['name']} {student['firstname']}<br>"
        if i == len(students) - 1:
            string_students_text += f"et {student['name']} {student['firstname']}"
        elif i == len(students) - 2:
            string_students_text += f"{student['name']} {student['firstname']} "
        else:
            string_students_text += f"{student['name']} {student['firstname']}, "

    with open(os.path.join(os.getcwd(), 'template', 'group_mail.html'), 'r', encoding="UTF-8") as f:
        body = f.read()

    body = body.replace(nom_session, session_dict['name_session'])
    body = body.replace(date_limit, session_dict['end_date_session'])
    body = body.replace(lien_choix_projet_template, lien_choix_projet_groupe)
    body = body.replace(list_etu, string_students)

    # -- Create Mail

    mail_list = []

    mail_text = (f"Votre groupe de projet pour {session_dict['name_session']} est composé de {string_students_text}.\n"
                 f"Vous pouvez désormais choisir vos préférences de projet en suivant le lien suivant "
                 f"{lien_choix_projet_groupe}.\n"
                 f"Pour plus d'informations, contactez votre professeur référent.\n"
                 f"\nEnvoyé avec ❤️ par l'équipe SmartChoice")

    for student in students:
        mail = {
            "from": {
                "email": os.getenv("MAIL"),
                "name": os.getenv("MAIL_NAME")
            },
            "to": [
                {
                    "email": student['email'],
                    "name": f"{student['firstname']} {student['name']}"
                }
            ],
            "subject": f"Votre groupe de projet pour {session_dict['name_session']}",
            "text": mail_text,
            "html": f"{body}",
        }
        mail_list.append(mail)

    return mail_list


@app.route('/api/send_mail_result', methods=['POST'])
def send_mail_result():
    """
    Decompose the send the result mail
    data = {
        "sessionID": 1,
        "group_project": {
            "1" : {
                "id_group" : "1",
                "id_project" : "2"
            },
            "2" : {
                "id_group" : "2",
                "id_project" : "1"
            }
        }
    };
    :return:
    """

    print("Enter sending result mails function")

    api_key = os.getenv("MAIL_API_KEY")
    mailer = emails.NewEmail(api_key)

    session_dict = get_session_data(session=request.json.get('sessionID'))
    students_all = get_all_groups_students(session=request.json.get('sessionID'))
    projects = get_all_projects(session=request.json.get('sessionID'))

    mail_list = []

    for group in request.json.get('group_project').values():
        projet_dict = {}  # initialize project dict
        id_group = -1
        students = {}
        for projet in projects:
            if projet["id"] == int(group['id_project']):  # find the project linked to the group
                projet_dict = projet

        for i, sous_group in enumerate(students_all.values()):
            if sous_group['id'] == int(group['id_group']):
                id_group = i + 1
                students = sous_group['students']

        if id_group != -1 and projet_dict != {} and students != {}:
            mail_list.append(send_mail_simple_result(session_dict, id_group, projet_dict, students))

    # Send mail
    response = mailer.send_bulk(mail_list)
    objects = response.split("\n")
    if len(objects) < 2:
        for obj in objects:
            data = json.loads(obj)
        status = objects[0]
        message = data["message"]
        bulk_email_id = data["bulk_email_id"]

        response = {
            "status": status,
            "message": message,
            "bulk_email_id": bulk_email_id,
            "bulk_email_status": mailer.get_bulk_status_by_id(bulk_email_id)
        }

        if status == 202:
            return jsonify({"result": response}), 200
        else:
            return jsonify({"error": response}), 500
    else:
        return jsonify({"error": response}), 500


def send_mail_simple_result(session_dict, id_group, project_dict, students):
    """
    Create the group mail to all the person of the group
    :param session_dict: dict containing all the information of the session
    :param id_group: id of the group
    :param project_dict: dict containing all the information of the project
    :param students: dict of all the students of the group
    :return:
    """
    # -- Replacing values using the template

    nom_session = "{{nom_session}}"  # session_dict['name_session']
    group = "{{group}}"
    name = "{{name}}"
    project_name = "{{project_name}}"
    project_description = "{{project_description}}"

    string_students = ""
    string_students_text = ""
    for i, student in enumerate(students):
        string_students += f"<li> {student['name']} {student['firstname']} <li>"
        if i == len(students) - 1:
            string_students_text += f"et {student['name']} {student['firstname']}"
        elif i == len(students) - 2:
            string_students_text += f"{student['name']} {student['firstname']} "
        else:
            string_students_text += f"{student['name']} {student['firstname']}, "

    with open(os.path.join(os.getcwd(), 'template', 'result_mail.html'), 'r', encoding="UTF-8") as f:
        body = f.read()

    body = body.replace(nom_session, session_dict['name_session'])
    body = body.replace(group, f"Groupe {id_group}")
    body = body.replace(name, string_students)
    body = body.replace(project_name, project_dict['nom'])
    body = body.replace(project_description, project_dict['description'])

    mail_text = (f"Votre groupe ({id_group}) composé de {string_students_text} a été assigné "
                 f"au projet {project_dict['nom']} ({project_dict['description']}).\n"
                 f"Contactez votre professeur référent pour plus de renseignement.\n"
                 f"\nEnvoyé avec ❤️ par l'équipe SmartChoice")

    # -- Create Mail

    mail_list = []

    for student in students:
        print(student)

        mail = {
            "from": {
                "email": os.getenv("MAIL"),
                "name": os.getenv("MAIL_NAME")
            },
            "to": [
                {
                    "email": student['email'],
                    "name": f"{student['firstname']} {student['name']}"
                }
            ],
            "subject": f"Votre projet pour {session_dict['name_session']}",
            "text": mail_text,
            "html": f"{body}",
        }
        mail_list.append(mail)

    print(mail_list)
    return mail_list


@app.route('/api/get_session_id', methods=['GET'])
def get_session_id():
    print('Enter get session ID function')
    # Il faut utiliser os.path.join pour que ce soit multiplateforme
    db = os.path.join(os.getcwd(), 'db', 'parcoursup.sqlite')
    if os.path.exists(db):
        try:
            session_id = request.args.get('sessionID')
            if not session_id:
                return jsonify({'error': 'Session ID parameter is missing'}), 400

            conn = sqlite3.connect(db)
            cursor = conn.cursor()
            
            cursor.execute("SELECT ID from SESSION where ID = " + (session_id,))

            response = cursor.fetchall()
            print(response)

            conn.close()

            # Convert data to JSON format
            return jsonify(response)

        except sqlite3.Error as e:
            return jsonify({'error': str(e)}), 500

    else:
        return jsonify({'error': "nul"}), 50


@app.route('/api/get_session_data', methods=['GET'])
def get_session_data():
    print('Enter get session data function')
    # Il faut utiliser os.path.join pour que ce soit multiplateforme
    db = os.path.join(os.getcwd(), 'db', 'parcoursup.sqlite')
    if os.path.exists(db):
        try:
            session_id = request.args.get('sessionID')
            if not session_id:
                return jsonify({'error': 'Session ID parameter is missing'}), 400

            conn = sqlite3.connect(db)
            cursor = conn.cursor()

            cursor.execute("SELECT * from SESSION where ID = ?", (session_id,))

            response = cursor.fetchall()
            print(response)

            session_dict = {
                'id': response[0][0],
                'name_session': response[0][1],
                'end_date_group': response[0][2],
                'end_date_session': response[0][3],
                'group_min': response[0][4],
                'group_max': response[0][5],
                'state': response[0][6],
                'fk_user': response[0][7],
            }

            conn.close()

            # Convert data to JSON format
            return jsonify(session_dict)

        except sqlite3.Error as e:
            return jsonify({'error': str(e)}), 500

    else:
        return jsonify({'error': "nul"}), 50


def get_session_data(session):
    print('Enter get session data function')
    # Il faut utiliser os.path.join pour que ce soit multiplateforme
    db = os.path.join(os.getcwd(), 'db', 'parcoursup.sqlite')
    if os.path.exists(db):
        try:
            session_id = session
            if not session_id:
                return jsonify({'error': 'Session ID parameter is missing'}), 400

            conn = sqlite3.connect(db)
            cursor = conn.cursor()

            cursor.execute("SELECT * from SESSION where ID = " + str(session_id))

            response = cursor.fetchall()
            print(response)

            session_dict = {
                'id': response[0][0],
                'name_session': response[0][1],
                'end_date_group': response[0][2],
                'end_date_session': response[0][3],
                'group_min': response[0][4],
                'group_max': response[0][5],
                'state': response[0][6],
                'fk_user': response[0][7],
            }

            conn.close()

            # Convert data to JSON format
            return session_dict

        except sqlite3.Error as e:
            return jsonify({'error': str(e)}), 500

    else:
        return jsonify({'error': "nul"}), 50


# -----------------------------------------------------------------------------

"""
data = {
    "men_preferences": {
        "man1": ["woman1", "woman2", "woman3"],
    },
    "women_preferences": {
        "woman1": ["man1", "man2", "man3"],
    }
}
"""


@app.route('/api/gale_shapley', methods=['POST'])
def gale_shapley_route():
    print(request.json)
    session_id = request.json.get('sessionID')
    print("Enter gale shapley")
    db = os.path.join(os.getcwd(), 'db', 'parcoursup.sqlite')
    print(db)
    if os.path.exists(db):
        conn = sqlite3.connect(db)
        cursor = conn.cursor()
        try:
            cursor.execute("""SELECT FK_Projet, FK_Groupe, Ordre_Preference FROM PREFERENCE_PROJET
                                        INNER JOIN PROJET ON PREFERENCE_PROJET.FK_Projet = PROJET.ID 
                                        WHERE PROJET.FK_Session = ?
                                        ORDER BY PREFERENCE_PROJET.FK_Projet, PREFERENCE_PROJET.Ordre_Preference;""",
                           (session_id,))
            projects_data = cursor.fetchall()

            def format_data(data):
                formated_data = {}
                for x, y, z in data:
                    if str(x) not in formated_data:
                        formated_data[str(x)] = [None, None, None]
                    formated_data[str(x)][z - 1] = str(y)
                return formated_data

            projects_preferencies = format_data(projects_data)

            cursor.execute("""SELECT FK_GROUPE, FK_Projet, Ordre_Preference FROM PREFERENCE_GROUPE
                            INNER JOIN GROUPE ON PREFERENCE_GROUPE.FK_Groupe = GROUPE.ID 
                            INNER JOIN PROJET ON PREFERENCE_GROUPE.FK_Projet = PROJET.ID
                            WHERE PROJET.FK_Session = ?
                            ORDER BY PREFERENCE_GROUPE.FK_Groupe, PREFERENCE_GROUPE.Ordre_Preference;""", (session_id,))

            groups_data = cursor.fetchall()

            groups_preferencies = format_data(groups_data)

            conn.close()

            data = {
                "men_preferences": groups_preferencies,
                "women_preferences": projects_preferencies,
            }

            if 'men_preferences' in data and 'women_preferences' in data:
                men_preferences = data['men_preferences']
                women_preferences = data['women_preferences']
                res = gale_shapley(women_preferences, men_preferences)

                return jsonify(res)
            else:
                return jsonify({'error': 'Invalid request'}), 400

        except sqlite3.Error as e:
            return jsonify({'error': str(e)}), 500


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


# -----------------------------------------------------------------------------

@app.route('/api/hello_world', methods=['GET'])
def get_hello_world():
    print('Enter test function')
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


######
# SESSION
######
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
            query_parameters = (
                session[0]['Nom'], session[0]['Deadline_Creation_Groupe'], session[0]['Deadline_Choix_Projet'],
                session[0]['Nb_Etudiant_Min'], session[0]['Nb_Etudiant_Max'], session[0]['Etat'],
                session[0]['FK_Utilisateur'])

            sql_request = cursor.execute("INSERT INTO SESSION VALUES (NULL, ?, ?, ?, ?, ?, ?, ?) RETURNING ID",
                                         query_parameters)
            session_id = sql_request.fetchone()
            # Commit the insertions
            conn.commit()
            conn.close()

            # Convert data to JSON format
            return jsonify({'result': session_id}), 200

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
    print('Enter update session function')
    # Retrieve parameters from the request body
    session_id = request.json.get('session_ID')
    session = request.json.get('data')

    # Il faut utiliser os.path.join pour que ce soit multiplateforme
    db = os.path.join(os.getcwd(), 'db', 'parcoursup.sqlite')
    if os.path.exists(db):
        conn = sqlite3.connect(db)
        cursor = conn.cursor()
        try:

            query_parameters = [(session[0]['Nom'], session[0]['Deadline_Creation_Groupe'],
                                 session[0]['Deadline_Choix_Projet'], session[0]['Nb_Etudiant_Min'],
                                 session[0]['Nb_Etudiant_Max'], session[0]['Etat'], session[0]['FK_Utilisateur'],
                                 session_id)]

            sql_request = cursor.execute(
                "UPDATE SESSION SET Nom = ?, Deadline_Creation_Groupe = ?, Deadline_Choix_Projet = ?, Nb_Etudiant_Min "
                "= ?, Nb_Etudiant_Max = ?, Etat = ?, FK_Utilisateur = ? WHERE ID = ?",
                query_parameters[0])
            session_id = sql_request.fetchone()

            # Commit the insertions
            conn.commit()
            conn.close()

            # Convert data to JSON format
            return jsonify({'result': session_id}), 200

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
    session_id = request.json.get('sessionID')  # json item

    # Il faut utiliser os.path.join pour que ce soit multiplateforme
    db = os.path.join(os.getcwd(), 'db', 'parcoursup.sqlite')
    if os.path.exists(db):
        conn = sqlite3.connect(db)
        cursor = conn.cursor()
        try:
            sql_request = cursor.execute("DELETE FROM SESSION WHERE ID = ?;", (session_id,))
            res = sql_request.fetchone()

            # Commit the delete
            conn.commit()
            conn.close()

            # Convert data to JSON format
            return jsonify({'result': res}), 200

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
            cursor.execute("SELECT id, Nom, Deadline_Choix_Projet, Etat FROM SESSION")

            response = cursor.fetchall()

            sessions = []
            for idx, session in enumerate(response):
                session_dict = {
                    'id': response[idx][0],
                    'nom': response[idx][1],
                    'end_date': response[idx][2],
                    'state': response[idx][3]
                }
                sessions.append(session_dict)

            conn.close()

            # Convert data to JSON format
            return jsonify(sessions)

        except sqlite3.Error as e:
            return jsonify({'error': str(e)}), 500

    else:
        return jsonify({'error': "nul"}), 50


######
# STUDENT
######
@app.route('/api/create_students', methods=['POST'])
def create_students():
    """
    Add all the students data from the csv file.
    Called right after the csv file of student is read.
    :return:
    """
    print('Enter create students function')

    # Retrieve parameters from the request body
    session_id = request.json.get('sessionID')  # assuming the parameters are sent in JSON format
    students = request.json.get('data')

    db = os.path.join(os.getcwd(), 'db', 'parcoursup.sqlite')
    if os.path.exists(db):
        conn = sqlite3.connect(db)
        cursor = conn.cursor()

        try:
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='ETUDIANT';")
            table_exists = cursor.fetchone() is not None

            if table_exists:
                cursor.execute(f"DELETE FROM ETUDIANT WHERE FK_Session ='{session_id}'")

            print(students)
            # Insert student data (without RETURNING)
            query_parameters = [(data['Nom'], data['Prenom'], data['Email'], session_id) for data in students]

            cursor.executemany(
                "INSERT INTO ETUDIANT (Nom, Prenom, Email, FK_Session) VALUES (?, ?, ?, ?)",
                query_parameters
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
    student_id = request.json.get('studentID')

    # Il faut utiliser os.path.join pour que ce soit multiplateforme
    db = os.path.join(os.getcwd(), 'db', 'parcoursup.sqlite')
    if os.path.exists(db):
        conn = sqlite3.connect(db)
        cursor = conn.cursor()
        try:
            sql_request = cursor.execute("SELECT FK_Groupe from ETUDIANT_GROUPE WHERE FK_Etudiant = ?", (student_id,))
            res = sql_request.fetchone()

            conn.close()

            if res is not None:
                res = True  # Déjà dans un groupe
            else:
                res = False  # Pas dans un groupe

            # Convert data to JSON format
            return jsonify({'result': res}), 200

        except sqlite3.Error as e:
            return jsonify({'error': str(e)}), 500
    else:
        return jsonify({'error': "nul"}), 50


@app.route('/api/get_all_students', methods=['POST'])
def get_all_students():
    """
    _summary_
    Method that retrieve all the students from a session.
        const data = {
            "sessionID" : 1
        };
        const jsonData = JSON.stringify(data);

        const response = await axios.post("http://127.0.0.1:5000/api/get_all_students", jsonData, {
          headers: {
            'Content-Type': 'application/json'
          }}
        );
    Returns:
    Json with all the students from a session
    """
    print('Enter get all students function')

    # Retrieve parameters from the request body
    session_id = request.json.get('sessionID')

    db = os.path.join(os.getcwd(), 'db', 'parcoursup.sqlite')
    if os.path.exists(db):
        conn = sqlite3.connect(db)
        cursor = conn.cursor()

        try:
            # Retrieve data from SQLite database
            cursor.execute("SELECT * FROM Etudiant WHERE FK_Session = ? ;", (session_id,))
            response = cursor.fetchall()

            # Prepare data for the front-end
            students = []
            for idx, student in enumerate(response):
                student_dict = {
                    'id': response[idx][0],
                    'name': response[idx][1],
                    'firstname': response[idx][2],
                    'email': response[idx][3],
                }
                students.append(student_dict)

            conn.close()

            # Convert data to JSON format
            return jsonify(students)

        except sqlite3.Error as e:
            return jsonify({'error': str(e)}), 500
    else:
        return jsonify({'error': "nul"}), 50


######
# PROJECT
######
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
            query_parameters = [(projet[0]['Nom'], projet[0]['Description'], projet[0]['Nb_Etudiant_Min'],
                                 projet[0]['Nb_Etudiant_Max'], projet[0]['FK_Session'])]

            sql_request = cursor.execute("INSERT INTO PROJET VALUES (NULL, ?, ?, ?, ?, ?) RETURNING ID",
                                         query_parameters[0])
            project_id = sql_request.fetchone()

            # Commit the insertions
            conn.commit()
            conn.close()

            # Convert data to JSON format
            return jsonify({'result': project_id}), 200

        except sqlite3.Error as e:
            return jsonify({'error': str(e)}), 500
    else:
        return jsonify({'error': "nul"}), 50


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
    project_id = request.json.get('projectID')  # json item

    # Il faut utiliser os.path.join pour que ce soit multiplateforme
    db = os.path.join(os.getcwd(), 'db', 'parcoursup.sqlite')
    if os.path.exists(db):
        conn = sqlite3.connect(db)
        cursor = conn.cursor()
        try:
            sql_request = cursor.execute("DELETE FROM PROJET WHERE ID = ?;", (project_id,))
            res = sql_request.fetchone()

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
    session_id = request.json.get('sessionID')

    db = os.path.join(os.getcwd(), 'db', 'parcoursup.sqlite')
    if os.path.exists(db):
        conn = sqlite3.connect(db)
        cursor = conn.cursor()

        try:
            # Retrieve data from SQLite database
            cursor.execute("SELECT * FROM Projet WHERE FK_Session = ? ;", (session_id,))
            response = cursor.fetchall()

            # Prepare data for the front-end
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


def get_all_projects(session):
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

    db = os.path.join(os.getcwd(), 'db', 'parcoursup.sqlite')
    if os.path.exists(db):
        conn = sqlite3.connect(db)
        cursor = conn.cursor()

        try:
            # Retrieve data from SQLite database
            cursor.execute("SELECT * FROM Projet WHERE FK_Session = ? ;", (session,))
            response = cursor.fetchall()

            # Prepare data for the front-end
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
            return projects

        except sqlite3.Error as e:
            return jsonify({'error': str(e)}), 500
    else:
        return jsonify({'error': "nul"}), 50


@app.route('/api/get_group_projects_order_by_preferencies', methods=['POST'])
def get_group_projects_order_by_preferencies():
    """
    _summary_
    Method that retrieve the projects from a session order by the group preferencies 
        const data = {
            "sessionID" : 1,
            "groupID" : 1,
        };
        const jsonData = JSON.stringify(data);

        const response = await axios.post("http://127.0.0.1:5000/api/get_group_projects_order_by_preferencies, jsonData,
         {
          headers: {
            'Content-Type': 'application/json'
          }}
        );
    Returns:
    Json with all the projects from a session order by the group preferencies
"""
    print('Enter group projects order by preferencies function')

    # Retrieve parameters from the request body
    session_id = request.json.get('sessionID')
    group_id = request.json.get('groupID')

    db = os.path.join(os.getcwd(), 'db', 'parcoursup.sqlite')
    if os.path.exists(db):
        conn = sqlite3.connect(db)
        cursor = conn.cursor()
        try:
            # Retrieve data from SQLite database
            cursor.execute("""SELECT * from PREFERENCE_GROUPE
                            INNER JOIN PROJET ON  PROJET.ID = PREFERENCE_GROUPE.FK_Projet 
                            WHERE FK_GROUPE = ? AND FK_Session = ?
                            ORDER BY PREFERENCE_GROUPE.Ordre_Preference;""", (group_id, session_id))

            response = cursor.fetchall()
            print("RESPONSEEEEEEEEEEE")
            print(sessionID)
            print(groupID)
            print(response)

            # Prepare data for the front-end
            projects = []
            for idx, project in enumerate(response):
                project_dict = {
                    'id': response[idx][4],
                    'nom': response[idx][5],
                    'description': response[idx][6],
                    'min_etu': response[idx][7],
                    'max_etu': response[idx][8],
                    'id_session': response[idx][9],
                    'date_derniere_modif': response[idx][3] 
                }
                projects.append(project_dict)

            conn.close()

            # Convert data to JSON format
            return jsonify(projects)

        except sqlite3.Error as e:
            return jsonify({'error': str(e)}), 500
    else:
        return jsonify({'error': "nul"}), 50


@app.route('/api/get_project_groups_order_by_preferencies', methods=['POST'])
def get_project_groups_order_by_preferencies():
    """
    _summary_
    Method that retrieve the groups order by the project preferencies 
        const data = {
            "sessionID" : 1,
            "projectID" : 1,
        };
        const jsonData = JSON.stringify(data);

        const response = await axios.post("http://127.0.0.1:5000/api/get_project_groups_order_by_preferencies, jsonData,
         {
          headers: {
            'Content-Type': 'application/json'
          }}
        );
    Returns:
    Json with all the groups order by the project preferencies
"""
    print('Enter project groups order by preferencies function')

    # Retrieve parameters from the request body
    session_id = request.json.get('sessionID')
    project_id = request.json.get('projectID')

    db = os.path.join(os.getcwd(), 'db', 'parcoursup.sqlite')
    if os.path.exists(db):
        conn = sqlite3.connect(db)
        cursor = conn.cursor()
        try:
            # Retrieve data from SQLite database
            cursor.execute("""SELECT * from PREFERENCE_PROJET
                            INNER JOIN GROUPE ON GROUPE.ID = PREFERENCE_PROJET.FK_Groupe 
                            WHERE FK_PROJET = ?
                            ORDER BY PREFERENCE_PROJET.Ordre_Preference;""", (project_id,))

            response = cursor.fetchall()

            cursor.execute("""
                    SELECT e.ID as 'StudentID', e.Nom, e.Prenom, e.Email, g.ID as 'GroupID' 
                    FROM ETUDIANT e
                    LEFT JOIN ETUDIANT_GROUPE eg ON e.ID = eg.FK_Etudiant
                    JOIN SESSION s ON e.FK_Session = s.ID
                    JOIN GROUPE g ON eg.FK_Groupe = g.ID
                    WHERE s.ID = ?;
                    """, (session_id,))

            groups_response = cursor.fetchall()
            groups = []
            print(response)
            for row in response:
                print(row)
                groups_dict = {
                    'id': row[1],
                    'students': [],
                }

                for student in groups_response:
                    print(student)
                    student_id, name, firstname, email, group_id = student  # Unpack data
                    if group_id == groups_dict['id']:
                        student_data = {
                            'id': student_id,
                            'firstname': firstname,
                            'name': name,
                            'email': email,
                        }
                        groups_dict['students'].append(student_data)

                groups.append(groups_dict)

            print(groups)

            conn.close()

            # Convert data to JSON format
            return jsonify(groups)

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
            query_parameters = [data['nom'],
                                data['description'],
                                data['min_etu'],
                                data['max_etu'],
                                data['id'],
                                data['id_session']
                                ]

            sql_request = cursor.execute(
                "UPDATE PROJET SET Nom = ?, Description = ?, Nb_Etudiant_Min = ?, Nb_Etudiant_Max = ? WHERE ID = ? "
                "and FK_Session = ?;",
                query_parameters)
            res = sql_request.fetchone()

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


@app.route('/api/affect_default_preferencies', methods=['POST'])
def affect_default_preferencies():
    """
    Methods that insert a group project's preference
    Example of data and post request to call in the front :
    const data = {
        "data": "sessionID" : 1
    }
    const jsonData = JSON.stringify(data);

    Returns:
    _type_: _description_
"""
    print('Enter affect default preferencies function')

    # Retrieve parameters from the request body
    session_id = request.json.get('data')  # assuming the parameters are sent in JSON format

    # Il faut utiliser os.path.join pour que ce soit multiplateforme
    db = os.path.join(os.getcwd(), 'db', 'parcoursup.sqlite')
    if os.path.exists(db):
        conn = sqlite3.connect(db)
        cursor = conn.cursor()

        try:
            cursor.execute("""SELECT DISTINCT FK_Groupe FROM ETUDIANT e
                    LEFT JOIN ETUDIANT_GROUPE eg ON e.ID = eg.FK_Etudiant
                    WHERE e.FK_Session = ?;""", (session_id,))

            groups = cursor.fetchall()

            cursor.execute("""SELECT id FROM Projet
                            WHERE FK_Session = ?;""", (session_id,))

            projects = cursor.fetchall()

            for project in projects:
                for idx, group in enumerate(groups):
                    project_id, group_id = project[0], group[0]
                    cursor.execute(
                        "INSERT INTO PREFERENCE_PROJET (FK_Projet, FK_Groupe, Ordre_Preference) VALUES (?, ?, ?)",
                        (project_id, group_id, idx + 1))
                    conn.commit()

            for group in groups:
                for idx, project in enumerate(projects):
                    print("enter!!")
                    print(group)
                    print(project)
                    group_id, project_id = group[0], project[0]
                    print(group_id, project_id)
                    cursor.execute(
                        "INSERT INTO PREFERENCE_GROUPE (FK_Groupe, FK_Projet, Ordre_Preference) VALUES (?, ?, ?)",
                        (group_id, project_id, idx + 1))
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
              "order": 2,
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
                cursor.execute("SELECT * FROM PREFERENCE_PROJET WHERE FK_Projet = ? AND FK_Groupe = ?",
                               (project_id, group_id))
                existing_row = cursor.fetchone()

                if existing_row:
                    # Update existing order
                    cursor.execute(
                        "UPDATE PREFERENCE_PROJET SET Ordre_Preference = ? WHERE FK_Projet = ? AND FK_Groupe = ?",
                        (order, project_id, group_id))
                else:
                    # Insert new preference
                    cursor.execute(
                        "INSERT INTO PREFERENCE_PROJET (FK_Projet, FK_Groupe, Ordre_Preference) VALUES (?, ?, ?)",
                        (project_id, group_id, order))

                conn.commit()
            conn.close()

            # Convert data to JSON format
            return jsonify({'result': "done"}), 200

        except sqlite3.Error as e:
            print(e)
            return jsonify({'error': str(e)}), 500
    else:
        return jsonify({'error': "nul"}), 50


######
# GROUP
######
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
    students_id = request.json.get(
        'data')  # Students ids members of the group assuming the parameters are sent in JSON format

    # Il faut utiliser os.path.join pour que ce soit multiplateforme
    db = os.path.join(os.getcwd(), 'db', 'parcoursup.sqlite')

    print(db)
    if os.path.exists(db):
        conn = sqlite3.connect(db)
        cursor = conn.cursor()
        try:
            # Create the group in the table GROUPE and return the ID
            sql_request = cursor.execute(
                "INSERT INTO GROUPE VALUES (NULL) RETURNING ID")
            group_id = sql_request.fetchone()

            # Insert in ETUDIANT_GROUPE table with the group ID
            query_parameters = [(data['studentID'], group_id[0]) for data in students_id]
            cursor.executemany("INSERT INTO ETUDIANT_GROUPE VALUES (?, ?)", query_parameters)

            # Commit the insertions
            conn.commit()
            conn.close()

            # Convert data to JSON format
            return jsonify({'result': group_id}), 200

        except sqlite3.Error as e:
            print(e)
            return jsonify({'error': str(e)}), 500
    else:
        return jsonify({'error': "nul"}), 50
    

@app.route('/api/delete_groups', methods=['POST'])
def delete_groups():
    """
    _summary_
        Method that delete a list of groups, take in parameter the ids.
    Returns:
        _type_: _description_
    """
    print('Enter delete groups function')
    # Retrieve parameters from the request body
    groups = request.json.get('groups')  # json item

    # Il faut utiliser os.path.join pour que ce soit multiplateforme
    db = os.path.join(os.getcwd(), 'db', 'parcoursup.sqlite')
    if os.path.exists(db):
        conn = sqlite3.connect(db)
        cursor = conn.cursor()
        try:
            for groupID in groups:
                sqlRequest = cursor.execute("DELETE FROM GROUPE WHERE ID = ?;", (groupID,))
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


@app.route('/api/get_all_groups_students', methods=['POST'])
def get_all_groups_students():
    """
        Methods that get all the groups and the students within it from single session

        Example of data and post request to call in the front :

            const data = {
            "sessionID" : 1
            }
            const jsonData = JSON.stringify(data);

            const response = await axios.post("http://127.0.0.1:5000/api/get_all_groups_students", jsonData, {
              headers: {
                'Content-Type': 'application/json'
              }}
            );

        Returns:
        _type_: _description_
        """
    print('Enter get all the groups and the students within it function')
    # Retrieve parameters from the request body
    session_id = request.json.get('sessionID')

    db = os.path.join(os.getcwd(), 'db', 'parcoursup.sqlite')
    if os.path.exists(db):
        conn = sqlite3.connect(db)
        cursor = conn.cursor()
        try:
            # Insert SQL query here
            sql = """
                    SELECT e.ID as 'StudentID', e.Nom, e.Prenom, e.Email, g.ID as 'GroupID' 
                    FROM ETUDIANT e
                    LEFT JOIN ETUDIANT_GROUPE eg ON e.ID = eg.FK_Etudiant
                    JOIN SESSION s ON e.FK_Session = s.ID
                    JOIN GROUPE g ON eg.FK_Groupe = g.ID
                    WHERE s.ID = ?;
                """

            # Execute the query with the session ID as a parameter
            cursor.execute(sql, (session_id,))

            # Build the output data structure
            groups = {}
            for row in cursor.fetchall():
                student_id, name, firstname, email, group_id = row  # Unpack data

                if group_id not in groups:
                    groups[group_id] = {
                        'id': group_id,
                        'students': [],
                    }
                student_data = {
                    'id': student_id,
                    'firstname': firstname,
                    'name': name,
                    'email': email,
                }
                groups[group_id]['students'].append(student_data)

            # Convert data to JSON format
            return jsonify(list(groups.values()))

        except sqlite3.Error as e:
            print(e)
            return jsonify({'error': str(e)}), 500
    else:
        return jsonify({'error': "nul"}), 500


def get_all_groups_students(session):
    """
        Local version of get_all_groups_students

        Returns:
        _type_: _description_
        """
    print('Enter get all the groups and the students within it function')

    # Retrieve parameters from the request body
    session_id = session

    db = os.path.join(os.getcwd(), 'db', 'parcoursup.sqlite')
    if os.path.exists(db):
        conn = sqlite3.connect(db)
        cursor = conn.cursor()
        try:
            # Insert SQL query here
            sql = """
                    SELECT e.ID as 'StudentID', e.Nom, e.Prenom, e.Email, g.ID as 'GroupID' 
                    FROM ETUDIANT e
                    LEFT JOIN ETUDIANT_GROUPE eg ON e.ID = eg.FK_Etudiant
                    JOIN SESSION s ON e.FK_Session = s.ID
                    JOIN GROUPE g ON eg.FK_Groupe = g.ID
                    WHERE s.ID = ?;
                """

            # Execute the query with the session ID as a parameter
            cursor.execute(sql, (session_id,))

            # Build the output data structure
            groups = {}
            for row in cursor.fetchall():
                student_id, name, firstname, email, group_id = row  # Unpack data

                if group_id not in groups:
                    groups[group_id] = {
                        'id': group_id,
                        'students': [],
                    }
                student_data = {
                    'id': student_id,
                    'firstname': firstname,
                    'name': name,
                    'email': email,
                }
                groups[group_id]['students'].append(student_data)

            # Convert data to JSON format
            return groups

        except sqlite3.Error as e:
            print(e)
            return jsonify({'error': str(e)})
    else:
        return jsonify({'error': "nul"})


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
            cursor.execute("SELECT FK_Etudiant FROM ETUDIANT_GROUPE")
            students = cursor.fetchall()

            print(students)

            
            for student in group:
                if(student['id_new_group'] == 0):
                    cursor.execute("DELETE FROM ETUDIANT_GROUPE WHERE FK_Etudiant=?", (student['id_student'],))
                elif(any(student['id_student'] in t for t in students)):
                    cursor.execute("UPDATE ETUDIANT_GROUPE SET FK_Groupe=? WHERE FK_Etudiant=?", (student['id_new_group'], student['id_student']))
                else :
                    cursor.execute("INSERT INTO ETUDIANT_GROUPE VALUES (?, ?)", (student['id_student'], student['id_new_group']))


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


@app.route('/api/affect_preference_group', methods=['POST'])
def affect_preference_group():
    """
    Methods that insert a group project's preference
    Example of data and post request to call in the front : 
    const data = {
        "data": [
            {
              "groupID": 1,
              "projectID": 1,
              "order": 1,
              "Date_Derniere_Modif": "12/02/2024"
            },
            {
              "groupID": 1,
              "projectID": 2,
              "order": 2,
              "Date_Derniere_Modif": "12/02/2024"
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
                group_id, project_id, order, date_derniere_modif = preference['groupID'], preference['projectID'], preference['order'], preference['Date_Derniere_Modif']

                # Check for existing entry with projectID and groupID
                existing_row = cursor.execute("SELECT * FROM PREFERENCE_GROUPE WHERE FK_Projet = ? AND FK_Groupe = ?",
                                              (project_id, group_id)).fetchone()

                if existing_row:
                    # Update existing order
                    cursor.execute(
                        "UPDATE PREFERENCE_GROUPE SET Ordre_Preference = ?, Date_Derniere_Modif = ? WHERE FK_Projet = ? AND FK_Groupe = ?",
                        (order, date_derniere_modif ,project_id, group_id))
                else:
                    # Insert new preference
                    cursor.execute(
                        "INSERT INTO PREFERENCE_GROUPE (FK_Groupe, FK_Projet, Ordre_Preference, Date_Derniere_Modif) VALUES (?, ?, ?, ?)",
                        (group_id, project_id, order, date_derniere_modif))

                conn.commit()
            conn.close()

            # Convert data to JSON format
            return jsonify({'result': "done"}), 200

        except sqlite3.Error as e:
            print(e)
            return jsonify({'error': str(e)}), 500
    else:
        return jsonify({'error': "can't find database"}), 50


if __name__ == '__main__':
    app.run(debug=True)
