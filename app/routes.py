from app import app, db
from flask import jsonify


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
    users = db.get_users_with_progress(3) #условный id == 3, как напишем авторизацию, тут будет current_user

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

