import psycopg
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
    def get_pages_in_module(id_track, number_module_in_track):
        with psycopg.connect(host=Config.DB_SERVER,
                             user=Config.DB_USER,
                             password=Config.DB_PASSWORD,
                             dbname=Config.DB_NAME) as con:

            cur = con.cursor()

            cur.execute('SELECT id FROM "module" WHERE id_track = %s AND numberInTrack = %s',
                        (id_track, number_module_in_track))

            id_module = cur.fetchall()

            cur.execute('SELECT * FROM page WHERE id_module = %s', (id_module,))

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
    def get_achievements(id_user):
        with psycopg.connect(host=Config.DB_SERVER,
                             user=Config.DB_USER,
                             password=Config.DB_PASSWORD,
                             dbname=Config.DB_NAME) as con:

            cur = con.cursor()

            cur.execute("SELECT * FROM userWithAchievements WHERE id_user = %s", (id_user,))

            result = cur.fetchall()

            if not result:
                print('achievements not found')
                return None
            return result

    @staticmethod
    def get_all_achievements():
        with psycopg.connect(host=Config.DB_SERVER,
                             user=Config.DB_USER,
                             password=Config.DB_PASSWORD,
                             dbname=Config.DB_NAME) as con:

            cur = con.cursor()

            cur.execute("SELECT * FROM achievements")

            result = cur.fetchall()

            if not result:
                print('achievements not found')
                return None
            return result


    @staticmethod
    def get_users_with_progress(id):
        with psycopg.connect(host=Config.DB_SERVER,
                             user=Config.DB_USER,
                             password=Config.DB_PASSWORD,
                             dbname=Config.DB_NAME) as con:

            cur = con.cursor()

            cur.execute("SELECT * FROM AppUser WHERE id != %s", (id,))

            result = cur.fetchall()
            if not result:
                print('users progress not found')
                return None
            return result

    @staticmethod
    def get_users_with_progress_with_cc():
        with psycopg.connect(host=Config.DB_SERVER,
                             user=Config.DB_USER,
                             password=Config.DB_PASSWORD,
                             dbname=Config.DB_NAME) as con:

            cur = con.cursor()

            cur.execute("SELECT * FROM AppUser")

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
                             dbname=Config.DB_NAME,
                             port=Config.DB_PORT) as con:

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
