import sqlite3
import hashlib

import params


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
                salted_pass = "admin" + str(1)
                hashed_pass = hashlib.sha256(salted_pass.encode())
                print(hashed_pass.hexdigest())

                insert = str(hashed_pass.hexdigest())
                cursor.execute("""
                            INSERT INTO User (
                            user_name, password)
                            VALUES ( 'admin', ? )
                            """, [insert])

            connection.commit()
            connection.close()
        except ConnectionError as error:
            print(error)

    @staticmethod
    def login(user_name, password):
        # return true if we find a valid login.
        # 1. find the user ID, given the username
        # the userID becomes the salt.
        # hash the given password + salt.
        # see if it exists in the DB for that user.
        # if so, return true.

        connection = sqlite3.connect('user')
        cursor = connection.cursor()

        # find the user_id so we can salt the password with the unique user ID

        find_user = cursor.execute("""
            SELECT user_id FROM User WHERE user_name = ?""", [user_name])

        # return false if no username match
        row = find_user.fetchone()
        if row == None:
            connection.close()
            return False
        # User ID is used as salt for the password
        user_id = row
        salted_password = password + str(user_id[0])
        # Hash the password
        hashed_password = hashlib.sha256(salted_password.encode())
        insert = (user_name, hashed_password.hexdigest())

        # Find if we have a match for user name and password
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

    @staticmethod
    def get_id(username):
        connection = sqlite3.connect('user')
        cursor = connection.cursor()

        # find the user_id so we can salt the password with the unique user ID
        find_user = cursor.execute("""
                    SELECT user_id FROM User WHERE user_name = ?""", [username])
        user_id = find_user.fetchone()
        return user_id[0]



