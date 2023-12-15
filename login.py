import sql
import bcrypt
import user
import getpass


def check(username, pw):
    username = sql.getuser(username)
    if username is not None:
        return bcrypt.checkpw(pw, username['Password'].encode())
    return False


def login():
    username = user.username_input("Username: ")
    password = getpass.getpass("Password: ")
    if username != "" and check(username, password.encode('utf-8')):
        print("Logged in\n")
        return True
    else:
        print("Incorrect Username or Password")
        print("Please try again\n")
        return False
