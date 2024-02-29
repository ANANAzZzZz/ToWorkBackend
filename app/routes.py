from app import app, db


@app.route('/')
def index():
    print(db.get_users())
    return "hello, world"
