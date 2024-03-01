import psycopg
from flask_login import current_user
from werkzeug.security import generate_password_hash
from config import Config


class DBInterface:
    @staticmethod
    def get_all_tracks():
        with psycopg.connect(host=Config.DB_SERVER,
                             user=Config.DB_USER,
                             password=Config.DB_PASSWORD,
                             dbname=Config.DB_NAME) as con:

            cur = con.cursor()

            cur.execute('SELECT * FROM track')

            result = cur.fetchall()

            if not result:
                print('users not found')
                return None
            return result

    @staticmethod
    def get_knowledge():
        with psycopg.connect(host=Config.DB_SERVER,
                             user=Config.DB_USER,
                             password=Config.DB_PASSWORD,
                             dbname=Config.DB_NAME) as con:

            cur = con.cursor()

            cur.execute('SELECT * FROM knowledge')

            result = cur.fetchall()

            if not result:
                print('users not found')
                return None
            return result
