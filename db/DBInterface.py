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
                print('tracks not found')
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
                print('knowledge not found')
                return None
            return result

    @staticmethod
    def get_modules(id_track):
        with psycopg.connect(host=Config.DB_SERVER,
                             user=Config.DB_USER,
                             password=Config.DB_PASSWORD,
                             dbname=Config.DB_NAME) as con:

            cur = con.cursor()

            cur.execute("SELECT * FROM module WHERE id_track = %s", (id_track,))

            result = cur.fetchall()

            if not result:
                print('modules not found')
                return None
            return result

    @staticmethod
    def get_users_with_progress(id):
        with psycopg.connect(host=Config.DB_SERVER,
                             user=Config.DB_USER,
                             password=Config.DB_PASSWORD,
                             dbname=Config.DB_NAME) as con:

            cur = con.cursor()

            cur.execute("SELECT * FROM user_with_progress WHERE id != %s", (id,))

            result = cur.fetchall()
            if not result:
                print('users progress not found')
                return None
            return result

    @staticmethod
    def get_login_password(name, password):
        with psycopg.connect(host=Config.DB_SERVER,
                             user=Config.DB_USER,
                             password=Config.DB_PASSWORD,
                             dbname=Config.DB_NAME) as con:

            cur = con.cursor()

            cur.execute("SELECT * FROM AppUser WHERE name = %s AND password = %s", (name, password))

            result = cur.fetchone()
            if not result:
                print('user not found')
                return None

            return result

    @staticmethod
    def add_user(name, password, last_name):
        with psycopg.connect(host=Config.DB_SERVER,
                             user=Config.DB_USER,
                             password=Config.DB_PASSWORD,
                             dbname=Config.DB_NAME) as con:

            cur = con.cursor()

            cur.execute("INSERT INTO AppUser (name, password,last_name, progress) VALUES (%s, %s, %s, %s) RETURNING name",
                        (name, password, last_name, 0))
            result = cur.fetchone()

            con.commit()

            if not result:
                return None

            return result

    @staticmethod
    def find_user_by_email(name):
        with psycopg.connect(host=Config.DB_SERVER,
                             user=Config.DB_USER,
                             password=Config.DB_PASSWORD,
                             dbname=Config.DB_NAME) as con:

            cur = con.cursor()

            cur.execute("SELECT * FROM AppUser WHERE name = %s", (name,))

            result = cur.fetchone()

            if not result:
                return None

            return result
