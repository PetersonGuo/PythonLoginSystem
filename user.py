import getpass
import sys
import re
import create
import login
import sql


def username_input(str1):
    print(str1)
    try:
        username = sys.stdin.readline().strip()
    except ValueError:
        print("Invalid Input")
        return ""
    if is_valid_username(username):
        return username
    return ""


def is_valid_username(str1):
    if len(str1) < 4:
        print("Username must be at least 4 characters long")
        return False
    elif len(str1) > 20:
        print("Username must be less than 20 characters long")
        return False
    elif re.search(r'[^A-Za-z0-9_.-]', str1):
        print("Invalid characters in username")
        return False
    else:
        return True


def is_valid_password(username, password):
    if len(password) < 12:
        print("Password must be at least 12 characters long")
        return False
    elif username in password:
        print("Password cannot contain your username")
        return False
    elif re.search(r'[^A-Za-z0-9!@#$%^&*()_+=-]', password):
        print("Invalid characters in password")
        return False
    else:
        return True


def yes_no_input():
    yn = ""
    try:
        yn = sys.stdin.readline()[0].lower()
    except ValueError:
        print("Invalid Input")
    return yn == "y"


def change_username(uid):  # Use password and 2fa to change username
    print("Are you sure you want to change your username? (y/n)")
    if yes_no_input():
        if __reauthenticate(uid):
            sql.change_username(uid, create.create_username())
            print('Username changed')
            return True
    print('Username not changed')
    return False


def change_password(uid):  # Use password and 2fa to change password
    print("Are you sure you want to change your password? (y/n)")
    if yes_no_input():
        if __reauthenticate(uid):
            sql.change_password(uid, create.create_password(sql.get_username(uid)))
            print('Password changed')
            return True
    print('Password not changed')
    return False


def delete_user(uid):  # Use password and 2fa to delete account
    print("Are you sure you want to delete your account? (y/n)")
    if yes_no_input():
        if __reauthenticate(uid):
            sql.delete_user(uid)
            print('Account deleted')
            return True
    print('Account not deleted')
    return False


def __reauthenticate(uid):
    password = getpass.getpass("Password: ")
    if login.check(sql.get_username(uid), password.encode('utf-8')):
        if sql.get_2fa_secret(uid) is not None:
            if login.twofactor_loop(uid):
                return True
        else:
            return True
    else:
        print("Incorrect Password")
    return False
