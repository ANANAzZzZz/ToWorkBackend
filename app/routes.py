from werkzeug.security import generate_password_hash

from app import app, db
from flask import jsonify, request, session
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, JWTManager, verify_jwt_in_request, \
    decode_token, get_jwt
import datetime

jwt = JWTManager(app)


def get_username_from_token(token):
    decoded_token = decode_token(token)
    username = decoded_token['sub']
    return username


@app.route("/registration", methods=["POST"])
def registration():
    data = request.get_json()
    if not data:
        return jsonify("Missing data"), 400

    username = data.get('name')
    last_name = data.get('last_name')
    password = data.get('password')
    user = db.find_user_by_email(username)
    if user:
        return jsonify("A user with such an email already exists")
    user = db.add_user(username,  generate_password_hash(password), last_name)
    if user:
        user_data = db.find_user_by_email(user[0])
        expires = datetime.timedelta(hours=24)
        access_token = create_access_token(identity=user_data[0], expires_delta=expires)
        return jsonify(access_token=access_token, id_user=user_data[0],
                       name_user=user_data[1], last_name_user=user_data[2], progress_user=user_data[4]), 200
    else:
        return jsonify(message='Неверные учетные данные'), 401


@app.route('/tracks')
@jwt_required()
def get_tracks():
    tracks = db.get_all_tracks()

    if not tracks:
        return []  #"No avaliable tracks"

    tracksList = []
    for track in tracks:
        dict = {
            'id': track[0],
            'name': track[1],
            'quantityModules': track[2]
        }
        tracksList.append(dict)
    return tracksList


@app.route('/knowledge')
@jwt_required()
def get_knowledge():
    knowledge = db.get_knowledge()

    if not knowledge:
        return [] # "No available knowledge"

    knowledgeList = []
    for k in knowledge:
        dict = {
            'id': k[0],
            'name': k[1],
            'content': k[2]
        }
        knowledgeList.append(dict)
    return knowledgeList


@app.route('/page_in_module/<int:id_track>/<int:number_module_in_track>')
@jwt_required()
def get_page_in_module(id_track, number_module_in_track):
    pages = db.get_pages_in_module(id_track, number_module_in_track)

    if not pages:
        return [] # "No available pages"

    pageList = []
    for p in pages:
        dict = {
            'id': p[0],
            'content': p[1],
            'name': p[2],
            'numberInModule': p[3],
            'idModule': p[4]
        }
        pageList.append(dict)
    return pageList


@app.route('/module/<int:id_track>')
@jwt_required()
def get_modules_on_track(id_track):
    modules = db.get_modules(id_track)

    if not modules:
        return [] # "No available modules"

    modulesList = []
    for k in modules:
        dict = {
            'id': k[0],
            'name': k[1],
            'quantityPage': k[2],
            'quantityCoin': k[3],
            'startContent': k[4],
            'endContent': k[5],
            'numberInTrack': k[6],
            'idTrack': k[7]
        }
        modulesList.append(dict)
    return modulesList


@app.route('/get_achievements', methods=["POST"])
@jwt_required()
def get_achievements():
    token = request.get_json()
    x = token['headers']['Authorization']
    x = x.replace('Bearer ', '')
    id_user = get_username_from_token(x)
    if not id_user:
        return "Invalid token"
    achievements = db.get_achievements(id_user)
    if not achievements:
        return [] # "No available achievements"

    achievementsList = []
    for k in achievements:
        dict = {
            'id': k[0],
            'id_user': k[1],
            'id_achievements': k[2],
        }
        achievementsList.append(dict)
    return achievementsList


@app.route('/get_all_achievements')
@jwt_required()
def get_all_achievements():
    achievements = db.get_all_achievements()
    if not achievements:
        return [] # "achievements not found"

    achievementsList = []
    for k in achievements:
        dict = {
            'id': k[0],
            'name': k[1],
            'description': k[2],
            'picture': k[3]
        }
        achievementsList.append(dict)
    return achievementsList


@app.route('/users_with_progress', methods=['POST'])
@jwt_required()
def get_users_with_progress():
    token = request.get_json()
    x = token['headers']['Authorization']
    x = x.replace('Bearer ', '')
    id_user = get_username_from_token(x)
    users = db.get_users_with_progress(id_user)

    if not users:
        return [] # "No available users"

    users_with_progress_list = []
    for k in users:
        dict = {
            'id': k[0],
            'name': k[1],
            'last_name': k[2],
            'progress': k[4]

        }
        users_with_progress_list.append(dict)
    return users_with_progress_list


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data:
        return "Bad request"
    username = data.get('name')
    password = data.get('password')

    user = db.get_login_password(username, password)
    if user:
        expires = datetime.timedelta(hours=24)
        access_token = create_access_token(identity=user[0], expires_delta=expires)
        return jsonify(access_token=access_token, id_user=user[0],
                       name_user=user[1], last_name_user=user[2], progress_user=user[4]), 200
    else:
        return jsonify(message='Неверные учетные данные'), 401


@app.route('/login_with_token', methods=['POST'])
@jwt_required()
def login_with_token():
    token = request.get_json()

    x = token['headers']['Authorization']
    x = x.replace('Bearer ', '')

    id_user = get_username_from_token(x)

    if not id_user:
        return jsonify(message='Bad token'), 401

    user = db.find_user_by_id(id_user)
    if not user:
        return jsonify(message='user not found'), 401

    expires = datetime.timedelta(hours=24)
    access_token = create_access_token(identity=id_user, expires_delta=expires)

    return jsonify(access_token=access_token, id_user=user[0], name_user=user[1], last_name_user=user[2], progress_user=user[4]), 200


@app.route('/need_registration', methods=['POST'])
def need_registration():
    data = request.get_json()
    mail = data.get('name')
    result = db.find_user_by_email(mail)

    if not result:
        return jsonify(message='the user was not found'), 200
    return jsonify(message='the user was found')


@app.route('/users_with_progress_with_cc', methods=['POST']) #current client
@jwt_required()
def get_users_with_progress_with_cc():
    users = db.get_users_with_progress_with_cc()

    if not users:
        return [] # "No available users"

    users_with_progress_list = []
    for k in users:
        dict = {
            'id': k[0],
            'name': k[1],
            'last_name': k[2],
            'progress': k[4]

        }
        users_with_progress_list.append(dict)
    return users_with_progress_list


@app.route('/get_last_modules', methods=['POST'])
@jwt_required()
def get_last_modules():
    token = request.get_json()
    x = token['headers']['Authorization']
    x = x.replace('Bearer ', '')
    id_user = get_username_from_token(x)
    if not id_user:
        return jsonify(message='bad token'), 401
    modules = db.get_last_modules(id_user)
    if not modules:
        return [] # jsonify('modules not found')

    modules_list = []
    for module in modules:
        dict = {
            'id_module': module[0],
            'id_track': module[1],
            'number_last_complete_page': module[2]
        }
        modules_list.append(dict)
    return modules_list


@app.route('/update_number_complete_page/<int:id_module>', methods=['POST'])
@jwt_required()
def update_number_complete_page(id_module):
    token = request.get_json()
    x = token['headers']['Authorization']
    x = x.replace('Bearer ', '')
    id_user = get_username_from_token(x)
    if not id_user:
        return jsonify(message='bad token'), 401
    page = db.update_number_complete_page(id_user, id_module)
    if not page:
        return jsonify(message='something went wrong'), 401
    return jsonify(message='success'), 200
