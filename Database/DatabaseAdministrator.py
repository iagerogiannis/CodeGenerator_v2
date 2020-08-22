from re import match

import mysql.connector
from pandas import DataFrame

from Database.SecurityProtocol import SecurityProtocol as sp
from Errors.DatabaseErrors import *
from Generic.MyJsonLib import MyJsonLib as jsonlib
from Generic.Generator import Generator as gen


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
        self.user_hkey = sp.en_hash(user_pass)

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

    def getUserData(self):
        self.cursor.execute("SELECT username, email FROM user WHERE user_id=%s", (int(self.user_id),))
        username, email = self.cursor.fetchone()
        return sp.aes_decrypt(username, self.admin_pass), sp.aes_decrypt(email, self.admin_pass)

    def validatePassword(self, password):

        self.cursor.execute("SELECT password FROM user WHERE user_id = {};".format(int(self.user_id)))
        pass_decrypted = sp.aes_decrypt(self.cursor.fetchone()[0], self.admin_pass)
        if sp.key2_is_correct(password, pass_decrypted):
            return True
        else:
            return False

    def attemptLogin(self, username, password):

        user_id = self.getUser(username)

        if user_id:
            self.cursor.execute("SELECT password FROM user WHERE user_id = {};".format(int(user_id),))
            pass_decrypted = sp.aes_decrypt(self.cursor.fetchone()[0], self.admin_pass)
            if sp.key2_is_correct(password, pass_decrypted):
                self.userLogin(user_id, password)
                return True

        return False

    def createUser(self, username, email, password):

        if username == "":
            raise EmptyUsernameError()

        if not match("^[A-Za-z0-9_-]*$", username):
            raise InvalidCharactersInUsernameError()

        users = self.getAllUsers()
        if not users.dropna().empty and True in list(users["username"].isin([username])):
            raise UsernameUsedError()

        if not users.dropna().empty and True in list(users["email"].isin([email])):
            raise EmailUsedError()

        if len(username) > 48 or len(username) < 6:
            raise UsernameLengthError

        if len(email) > 48:
            raise EmailLengthError

        if len(password) > 48 or len(password) < 6:
            raise PasswordLengthError

        # Create user
        self.cursor.execute("INSERT INTO user (username, email, password) VALUES (%s, %s, %s);",
                            (sp.aes_encrypt(username, self.admin_pass),
                             sp.aes_encrypt(email, self.admin_pass),
                             sp.aes_encrypt(sp.protected_key_2(password), self.admin_pass),))

        self.connection.commit()

    def editUser(self, data, value):

        def username_query():
            nonlocal data, value
            self.cursor.execute("UPDATE user SET username = %s WHERE user_id = %s;",
                                (sp.aes_encrypt(value, self.admin_pass), int(self.user_id),))

        def email_query():
            nonlocal data, value
            self.cursor.execute("UPDATE user SET email = %s WHERE user_id = %s;",
                                (sp.aes_encrypt(value, self.admin_pass), int(self.user_id),))

        def password_query():
            nonlocal data, value
            self.cursor.execute("UPDATE user SET password = %s WHERE user_id = %s;",
                                (sp.aes_encrypt(sp.protected_key_2(value), self.admin_pass),
                                 int(self.user_id),))

        def edit_password_by_id(pass_id):
            nonlocal value

            def generate_salt():
                nonlocal setup
                return gen.produce_code(setup)

            def get_salt():
                nonlocal salts_file, pass_id
                return jsonlib.locate_by_id(salts_file, "password_id", pass_id)["salt"]

            def overwrite_salt():
                nonlocal pass_id, salts_file, salt
                salt_data = {"password_id": int(pass_id), "salt": salt}
                jsonlib.overwrite_by_id(salts_file, "password_id", int(pass_id), salt_data)

            def get_password():
                nonlocal pass_id
                self.cursor.execute("SELECT password FROM password WHERE password_id = %s;", (int(pass_id),))
                return sp.aes_decrypt(sp.aes_decrypt(self.cursor.fetchone()[0], self.admin_pass, decode=False),
                                      sp.protected_key_1(self.user_hkey, get_salt()))

            def edit_password():
                nonlocal pass_id, salt
                password = get_password()
                self.cursor.execute("UPDATE password SET password = %s WHERE password_id = %s;",
                                    (sp.aes_encrypt(sp.aes_encrypt(password, sp.protected_key_1(sp.en_hash(value), salt)),
                                                    self.admin_pass),
                                     int(pass_id),))
                self.connection.commit()

            salts_file = "{}/{}".format("Database", "salts.json")
            setups_file = "{}/{}".format("Database", "setups.json")
            setup = jsonlib.read_json(setups_file)[0]

            salt = generate_salt()
            edit_password()
            overwrite_salt()

        def get_password_ids():
            self.cursor.execute("SELECT password_id FROM password WHERE user_id = %s;", (int(self.user_id), ))
            return [int(id_value[0]) for id_value in self.cursor.fetchall()]

        if data == "username":
            username_query()
        elif data == "email":
            email_query()
        elif data == "password":
            for password_id in get_password_ids():
                edit_password_by_id(password_id)
            password_query()
            self.user_hkey = value

        self.connection.commit()

    def checkUserData(self, data, value):

        if data == "username":
            if value == "":
                raise EmptyUsernameError()
            if not match("^[A-Za-z0-9_-]*$", value):
                raise InvalidCharactersInUsernameError()
            users = self.getAllUsers()
            if not users.dropna().empty and True in list(users["username"].isin([value])):
                raise UsernameUsedError()
            if len(value) > 48 or len(value) < 6:
                raise UsernameLengthError

        elif data == "email":
            users = self.getAllUsers()
            if not users.dropna().empty and True in list(users["email"].isin([value])):
                raise EmailUsedError()
            if len(value) > 48 or len(value) < 6:
                raise EmailLengthError

        elif data == "password":
            if len(value) > 48 or len(value) < 6:
                raise PasswordLengthError

    def removeUser(self):

        def get_password_ids():
            self.cursor.execute("SELECT password_id FROM password WHERE user_id = %s;", (int(self.user_id), ))
            return [int(id_value[0]) for id_value in self.cursor.fetchall()]

        for pass_id in get_password_ids():
            self.removePassword(pass_id)

        self.cursor.execute("DELETE FROM user WHERE user_id = %s;", (self.user_id,))
        self.connection.commit()

    def checkPasswordEntry(self, account, username, email):

        if len(account) > 48 or len(account) < 2:
            raise PassAccountLengthError

        if len(username) > 48:
            raise PassUsernameLengthError

        if len(email) > 48:
            raise PassEmailLengthError

    def addPassword(self, account, username, email, password):

        def generate_salt():
            setups_file = "{}/{}".format("Database", "setups.json")
            setup = jsonlib.read_json(setups_file)[0]
            return gen.produce_code(setup)

        def append_salt():
            nonlocal salt
            data = {"password_id": self.getLastIndex(), "salt": salt}
            file = "{}/{}".format("Database", "salts.json")
            jsonlib.append_to_json(data, file)

        self.checkPasswordEntry(account, username, email)
        salt = generate_salt()

        self.cursor.execute("INSERT INTO password (account, username, email, password, user_id) "
                            "VALUES (%s, %s, %s, %s, %s);",
                            (sp.aes_encrypt(account, self.admin_pass),
                             sp.aes_encrypt(username, self.admin_pass),
                             sp.aes_encrypt(email, self.admin_pass),
                             sp.aes_encrypt(
                                 sp.aes_encrypt(password,
                                                sp.protected_key_1(self.user_hkey, salt)),
                                 self.admin_pass),
                             self.user_id,))

        append_salt()

        self.connection.commit()

    def editPassword(self, pass_id, account, username, email, password):

        def generate_salt():
            setups_file = "{}/{}".format("Database", "setups.json")
            setup = jsonlib.read_json(setups_file)[0]
            return gen.produce_code(setup)

        def overwrite_salt():
            nonlocal pass_id
            file = "{}/{}".format("Database", "salts.json")
            data = {"password_id": int(pass_id), "salt": salt}
            jsonlib.overwrite_by_id(file, "password_id", int(pass_id), data)

        self.checkPasswordEntry(account, username, email)
        salt = generate_salt()
        overwrite_salt()

        self.cursor.execute("UPDATE password SET account = %s, username = %s, email = %s, password = %s "
                            "WHERE password_id = %s;",
                            (sp.aes_encrypt(account, self.admin_pass),
                             sp.aes_encrypt(username, self.admin_pass),
                             sp.aes_encrypt(email, self.admin_pass),
                             sp.aes_encrypt(sp.aes_encrypt(password,
                                                           sp.protected_key_1(self.user_hkey, salt)),
                                            self.admin_pass),
                             int(pass_id),))

        self.connection.commit()

    def removePassword(self, pass_id):

        def remove_salt():
            file = "{}/{}".format("Database", "salts.json")
            jsonlib.drop_by_id(file, "password_id", pass_id)

        remove_salt()
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
                                                      sp.protected_key_1(self.user_hkey, getSalt(password)))
                                       for password in passwords]
                          })

    def getLastIndex(self):
        self.cursor.execute("SELECT LAST_INSERT_ID();")
        return int(self.cursor.fetchone()[0])
