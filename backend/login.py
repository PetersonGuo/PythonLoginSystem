import os
import bcrypt
import getpass
import time

import create
import sql
import twofactor
import User


def check(user, pw):
    time.sleep(os.urandom(1)[0] / 1000)
    return user.uid is not None and bcrypt.checkpw(pw, sql.get_encoded_pw(user).encode())


def login():
    username = create.username_input("Username: ")
    password = getpass.getpass("Password: ")
    possible_user = User.User(sql.get_user_id(username), username)
    if username != "" and check(possible_user, password.encode('utf-8')):
        if sql.get_2fa_secret(possible_user) is not None:
            if not twofactor_loop(possible_user):
                return None
        print("Logged in\n")
        return possible_user
    else:
        print("Incorrect Username or Password")
        print("Please try again\n")
        return None


def twofactor_loop(user):
    tries = 0
    while tries < 3:
        if twofactor.verify_code(sql.get_2fa_secret(user)):
            return True
        print("Incorrect 2FA Code")
        if tries < 2:
            print("Please try again\n")
        else:
            print("Too many attempts, please try again later\n")
        tries += 1
    return False
