import psycopg
from config import Config
from werkzeug.security import check_password_hash


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

            cur.execute('SELECT id FROM "module" WHERE idTrack = %s AND numberInTrack = %s',
                        (id_track, number_module_in_track))

            id_module = cur.fetchone()

            cur.execute('SELECT * FROM page WHERE idModule = %s', (id_module[0],))

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

            cur.execute("SELECT * FROM module WHERE idTrack = %s", (id_track,))

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

            cur.execute("SELECT * FROM achievement")

            result = cur.fetchall()

            if not result:
                print('achievements not found')
                return None
            return result

    @staticmethod
    def get_users_with_progress(user_id):
        with psycopg.connect(host=Config.DB_SERVER,
                             user=Config.DB_USER,
                             password=Config.DB_PASSWORD,
                             dbname=Config.DB_NAME) as con:

            cur = con.cursor()

            cur.execute("SELECT * FROM AppUser WHERE id != %s", (user_id,))

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

            cur.execute("SELECT * FROM AppUser WHERE name = %s", (name,))

            user = cur.fetchone()

            if not user:
                print('user not found')
                return None

            if not check_password_hash(user[3], password):
                print('wrong password')
                return None

            return user

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

    @staticmethod
    def get_last_modules(user_id):
        with psycopg.connect(host=Config.DB_SERVER,
                             user=Config.DB_USER,
                             password=Config.DB_PASSWORD,
                             dbname=Config.DB_NAME) as con:

            cur = con.cursor()

            cur.execute("""
                SELECT t1.id_module, t2.idTrack
                FROM user_progress_in_module AS t1
                JOIN "module" AS t2 ON t1.id_module = t2.id
                WHERE t1.numberLastCompletePage <> t2.quantityPage AND t1.id_user = %s;
            """, (user_id,))

            result = cur.fetchall()

            if not result:
                return None

            return result

    @staticmethod
    def update_number_complete_page(user_id, module_id):
        with psycopg.connect(host=Config.DB_SERVER,
                             user=Config.DB_USER,
                             password=Config.DB_PASSWORD,
                             dbname=Config.DB_NAME) as con:

            cur = con.cursor()

            cur.execute("UPDATE user_progress_in_module SET numberLastCompletePage = numberLastCompletePage + 1 "
                        "WHERE id_user = %s AND id_module = %s RETURNING numberLastCompletePage" , (user_id, module_id) )

            result = cur.fetchone()

            con.commit()

            if not result:
                return None

            return result

    @staticmethod
    def find_user_by_id(id_user):
        with psycopg.connect(host=Config.DB_SERVER,
                             user=Config.DB_USER,
                             password=Config.DB_PASSWORD,
                             dbname=Config.DB_NAME) as con:

            cur = con.cursor()

            cur.execute("SELECT * FROM AppUser WHERE id = %s", (id_user,))

            result = cur.fetchone()

            if not result:
                return None

            return result