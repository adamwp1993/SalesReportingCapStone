import sqlite3

class Database:

# TODO - hash passwords in DB. no plain text passwords!

    def __init__(self):
        """"""
        connection = None

        try:
            connection = sqlite3.connect('user')
            cursor = connection.cursor()
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS User(
            user_id INTEGER PRIMARY KEY, user_name TEXT NOT NULL UNIQUE, password TEXT NOT NULL ); ''')
            connection.commit()

            # Create the default admin login if it does not already exist
            result = cursor.execute("""SELECT * FROM User WHERE user_name = 'admin'
            """)
            if len(result.fetchall()) == 0:
                cursor.execute('''
                            INSERT INTO User (
                            user_name, password)
                            VALUES ( 'admin', 'admin' )
                            ''')

            connection.commit()
            connection.close()
        except ConnectionError as error:
            print(error)

    @staticmethod
    def login(user_name, password):
        # return true if we find a valid login.
        insert = (user_name, password)
        connection = sqlite3.connect('user')
        cursor = connection.cursor()
        rows = cursor.execute("""
        SELECT * FROM User WHERE user_name = ? AND password = ?""", insert)
        if len(rows.fetchall()) > 0:
            connection.close()
            return True
        else:
            connection.close()
            return False

    @staticmethod
    def query_users():
        connection = sqlite3.connect('user')
        cursor = connection.cursor()
        rows = cursor.execute("""
        SELECT * FROM User
        """)
        for row in rows:
            print(row)
        connection.close()


