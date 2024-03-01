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
