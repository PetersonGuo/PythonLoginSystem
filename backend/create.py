import user
import User
import sql

import re
import sys
import bcrypt
import getpass
from verify_email import verify_email


def create_account():
    username = create_username()
    email = email_input("Enter your email address: ")
    uid = sql.insert_email(username, email, create_password(username))
    session_user = User.User(uid, username, email)
    print("\nWould you like to setup 2FA? (y/n)")
    if user.yes_no_input():
        session_user.setup_2fa()
    print("User created Successfully\n")


def username_input(str1: str):
    print(str1)
    try:
        username = sys.stdin.readline().strip()
    except ValueError:
        print("Invalid Input")
        return ""
    if is_valid_username(username):
        return username
    return ""


def is_valid_username(str1: str):
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


def email_input(str1: str):
    print(str1)
    try:
        email = sys.stdin.readline().strip()
    except ValueError:
        print("Invalid Input")
        return ""
    if verify_email(email):
        return email
    return ""


def create_username():
    username = ""
    while username == "":
        username = username_input("Enter a new username: ")
        if len(username) == 0:
            continue
        elif sql.get_user_id(username) is not None:
            print("That username is already taken")
            username = ""
    return username


def is_valid_password(username: str, password):
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


def create_password(username: str):
    print(
        "\nDo not use common passwords\nUse Letters, Numbers, and Symbols\nDo not use common "
        "english words in your password\nDo not use your name, username, birthday, or other personal "
        "information\nMust be at least 12 characters long")

    pw = ""
    while pw == "":
        pw = getpass.getpass('\nEnter a new password: ')
        if is_valid_password(username, pw):
            pw2 = getpass.getpass('Confirm password: ')
            if pw == pw2:
                break
            else:
                print("Passwords do not match")
                pw = ""
        else:
            pw = ""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(pw.encode('utf-8'), salt)
