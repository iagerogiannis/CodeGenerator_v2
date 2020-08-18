from re import match

import mysql.connector
from pandas import DataFrame

from Database.SecurityProtocol import SecurityProtocol as sp
from Errors.DatabaseErrors import *
from Generic.MyJsonLib import MyJsonLib as jsonlib


class DatabaseAdministrator:

    connection: mysql.connector.connection.MySQLConnection
    cursor: mysql.connector.connection.MySQLCursor

    def __init__(self):
        self.admin_pass = self.get_admin_password()
        self.initialize()
        self.userLogin(0, "")

    def get_admin_password(self):
        pass_file = "{}/{}".format("Database", "admin_pass.json")
        return jsonlib.read_json(pass_file)["admin_password"]

    def initialize(self):
        self.connect()
        self.cursor = self.connection.cursor()

    def connect(self):
        self.connection = mysql.connector.connect(
            host="localhost",
            user="code_generator_admin",
            password=self.admin_pass,
            database="code_generator_db",
            raw=True
        )

    def userLogin(self, user_id, user_pass):
        self.user_id = int(user_id)
        self.user_pass = user_pass

    def getAllUsers(self):

        self.cursor.execute("SELECT user_id, username, email FROM user;")

        users = self.cursor.fetchall()

        return DataFrame({"id": [user[0] for user in users],
                          "username": [sp.aes_decrypt(user[1], self.admin_pass) for user in users],
                          "email": [sp.aes_decrypt(user[2], self.admin_pass) for user in users]})

    def getUser(self, username):

        users = self.getAllUsers()

        if username in list(users["username"]):
            return users.loc[users["username"] == username]["id"].values[0]
        else:
            return None

    def attemptLogin(self, username, password):

        user_id = self.getUser(username)

        if user_id:
            self.cursor.execute("SELECT password FROM user WHERE user_id = {};".format(int(user_id),))
            pass_decrypted = sp.aes_decrypt(self.cursor.fetchone()[0], self.admin_pass)
            if sp.key2_is_correct(password, pass_decrypted):
                self.userLogin(user_id, password)
                return True

        return False

    def createAccount(self, username, email, password):

        if username == "":
            raise EmptyUsernameError()

        if not match("^[A-Za-z0-9_-]*$", username):
            raise InvalidCharactersInUsernameError()

        users = self.getAllUsers()
        if not users.dropna().empty and True in list(users["username"].isin([username])):
            raise UsernameUsedError()

        if not users.dropna().empty and True in list(users["email"].isin([email])):
            raise EmailUsedError()

        # Create user
        self.cursor.execute("INSERT INTO user (username, email, password) VALUES (%s, %s, %s);",
                            (sp.aes_encrypt(username, self.admin_pass),
                             sp.aes_encrypt(email, self.admin_pass),
                             sp.aes_encrypt(sp.protected_key_2(password), self.admin_pass),))

        self.connection.commit()

    def addSetup(self):
        pass

    def editSetup(self):
        pass

    def removeSetup(self):
        pass

    def getSetups(self):
        pass

    def addPassword(self, account, username, email, password):

        def append_salt():
            nonlocal salt
            data = {"password_id": self.getLastIndex(), "salt": salt.decode("utf-8")}
            file = "{}/{}".format("Database", "salts.json")
            jsonlib.append_to_json(data, file)

        salt = sp.generate_salt()

        self.cursor.execute("INSERT INTO password (account, username, email, password, user_id) "
                            "VALUES (%s, %s, %s, %s, %s);",
                            (sp.aes_encrypt(account, self.admin_pass),
                             sp.aes_encrypt(username, self.admin_pass),
                             sp.aes_encrypt(email, self.admin_pass),
                             sp.aes_encrypt(
                                 sp.aes_encrypt(password, sp.protected_key_1(self.user_pass, salt)),
                                 self.admin_pass),
                             self.user_id,))

        append_salt()

        self.connection.commit()

    def editPassword(self, pass_id, account, username, email, password):

        def overwrite_salt():
            nonlocal pass_id, salt
            file = "{}/{}".format("Database", "salts.json")
            data = {"password_id": int(pass_id), "salt": salt.decode('utf-8')}
            jsonlib.overwrite_by_id(file, "password_id", int(pass_id), data)

        salt = sp.generate_salt()
        overwrite_salt()

        self.cursor.execute("UPDATE password SET account = %s, username = %s, email = %s, password = %s "
                            "WHERE password_id = %s;",
                            (sp.aes_encrypt(account, self.admin_pass),
                             sp.aes_encrypt(username, self.admin_pass),
                             sp.aes_encrypt(email, self.admin_pass),
                             sp.aes_encrypt(
                                 sp.aes_encrypt(password, sp.protected_key_1(self.user_pass, salt)),
                                 self.admin_pass),
                             int(pass_id),))

        # self.cursor.execute("SELECT * FROM password WHERE password_id = %s", (int(pass_id),))
        # print(self.cursor.fetchall())

        self.connection.commit()

    def removePassword(self, pass_id):
        self.cursor.execute("DELETE FROM password WHERE password_id = %s;", (pass_id,))
        self.connection.commit()

    def getPasswords(self):

        def getSalt(password):
            file = "{}/{}".format("Database", "salts.json")
            return jsonlib.locate_by_id(file, "password_id", int(password[0]))["salt"]

        self.cursor.execute("SELECT * FROM password WHERE user_id = %s", (self.user_id,))
        passwords = self.cursor.fetchall()

        return DataFrame({"ID": [str(int(password[0])) for password in passwords],
                          "Account": [sp.aes_decrypt(password[1], self.admin_pass) for password in passwords],
                          "Username": [sp.aes_decrypt(password[2], self.admin_pass) for password in passwords],
                          "Email": [sp.aes_decrypt(password[3], self.admin_pass) for password in passwords],
                          "Password": [sp.aes_decrypt(sp.aes_decrypt(password[4], self.admin_pass, decode=False),
                                                       sp.protected_key_1(self.user_pass,
                                                                          getSalt(password).encode('utf-8')))
                                       for password in passwords]
                          })

    def getLastIndex(self):
        self.cursor.execute("SELECT LAST_INSERT_ID();")
        return int(self.cursor.fetchone()[0])
