import sql
import bcrypt
import user
import getpass
import twofactor


def check(username, pw):
    uid = sql.get_user_id(username)
    if uid is not None:
        return bcrypt.checkpw(pw, sql.get_encoded_pw(uid).encode())
    return False


def login():
    username = user.username_input("Username: ")
    password = getpass.getpass("Password: ")
    if username != "" and check(username, password.encode('utf-8')):
        uid = sql.get_user_id(username)
        if sql.get_2fa_secret(uid) is not None:
            if not twofactor_loop(uid):
                return None
        print("Logged in\n")
        return uid
    else:
        print("Incorrect Username or Password")
        print("Please try again\n")
        return None


def twofactor_loop(uid):
    tries = 0
    while tries < 3:
        if twofactor.verify_code(sql.get_2fa_secret(uid)):
            return True
        print("Incorrect 2FA Code")
        if tries < 2:
            print("Please try again\n")
        else:
            print("Too many attempts, please try again later\n")
        tries += 1
    return False
