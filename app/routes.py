from app import app, db
from flask import jsonify, request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, JWTManager

jwt = JWTManager(app)


@app.route("/registration", methods=["POST"])
def registration():
    data = request.get_json()
    username = data.get('name')
    last_name = data.get('last_name')
    password = data.get('password')
    user = db.add_user(username,  password, last_name)
    if user:
        user_data = db.find_user_by_email(user[0])
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token, id_user=user_data[0],
                       name_user=user_data[1], last_name_user=user_data[2],progress_user=user_data[4]), 200
    else:
        return jsonify(message='Неверные учетные данные'), 401


@app.route('/tracks')
def get_tracks():
    tracks = db.get_all_tracks()

    if not tracks:
        return "No avaliable tracks"

    tracksList = []
    for track in tracks:
        dict = {
            'id': track[0],
            'name': track[1]
        }
        tracksList.append(dict)
    return tracksList


@app.route('/knowledge')
@jwt_required()
def get_all_tracks():
    knowledge = db.get_knowledge()

    if not knowledge:
        return "No available knowledge"

    knowledgeList = []
    for k in knowledge:
        dict = {
            'id': k[0],
            'name': k[1],
            'content': k[2]
        }
        knowledgeList.append(dict)
    return knowledgeList


@app.route('/module/<int:id_track>')
@jwt_required()
def get_modules_on_track(id_track):
    modules = db.get_modules(id_track)

    if not modules:
        return "No available modules"

    modulesList = []
    for k in modules:
        dict = {
            'id': k[0],
            'name': k[1],
            'content': k[2],
            'html': k[3],
            'id_track': k[4]

        }
        modulesList.append(dict)
    return modulesList


@app.route('/users_with_progress')
def get_users_with_progress():
    users = db.get_users_with_progress(0) #условный id == 3, как напишем авторизацию, тут будет current_user

    if not users:
        return "No available users"

    users_with_progress_list = []
    for k in users:
        dict = {
            'id': k[0],
            'name': k[1],
            'last_name': k[2],
            'progress': k[3]

        }
        users_with_progress_list.append(dict)
    return users_with_progress_list


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('name')
    password = data.get('password')

    user = db.get_login_password(username, password)
    if user:
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token, id_user=user[0],
                       name_user=user[1], last_name_user=user[2], progress_user=user[4]), 200
    else:
        return jsonify(message='Неверные учетные данные'), 401


# @app.route('/login_with_token', methods=['POST'])
# @jwt_required()
# def login_with_token():
#     token = request.get_json()
#
#     return token
# #     current_user = get_jwt_identity()
# #     return jsonify(logged_in_as=current_user), 200

