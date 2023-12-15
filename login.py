# To Implement:
# User Timeout/Brute force prevention
# User account control
# 2FA
# Password strength
# Error catching with SQL
# frontend and flask

import sys
import os
import re
import bcrypt
import pymysql.cursors
from dotenv import load_dotenv
import getpass

load_dotenv()


def connect():
    return pymysql.connect(host=os.getenv('database_host'),
                           user=os.getenv('database_user'),
                           password=os.getenv('database_pass'),
                           database=os.getenv('database_name'),
                           cursorclass=pymysql.cursors.DictCursor)


def getuser(username):
    conn = connect()
    with conn:
        sql = "SELECT * FROM `User` WHERE `Username`=%s"
        conn.ping()
        with conn.cursor() as cursor:
            cursor.execute(sql, username)
            result = cursor.fetchone()

    return result


def username_input(str1):
    print(str1)
    username = sys.stdin.readline().strip()
    if is_valid_username(username):
        return username
    return ""


def check(username, pw):
    user = getuser(username)
    if user is not None:
        return bcrypt.checkpw(pw, user['Password'].encode())
    return False


def is_valid_username(str1):
    print("Invalid characters in username")
    return re.search(r'^[A-Za-z0-9_.-]+$', str1)


def create():
    username = ""
    while username == "":
        username = username_input("Enter a new username: ")
        if len(username) == 0:
            continue
        elif getuser(username) is not None:
            print("That username is already taken")
            username = ""

    print(
        "\nDo not use common passwords\nUse Letters, Numbers, and Symbols\nDo not use common "
        "english words in your password\nDo not use your name, username, birthday, or other personal "
        "information\nMust be at least 12 characters long")

    pw = ""
    while pw == "":
        print("\nEnter a new password: ")
        pw = getpass.getpass('\nEnter a new password: ')
        if len(pw) < 12:
            print("Password must be at least 12 characters long")
            pw = ""
        elif username in pw:
            print("Password cannot contain your username")
            pw = ""

    salt = bcrypt.gensalt()
    pwhash = bcrypt.hashpw(pw.encode('utf-8'), salt)
    salt = ""
    pw = ""

    conn = connect()
    with conn:
        sql = "INSERT INTO `User` (Username, Password) VALUES (%s, %s)"
        conn.ping()
        with conn.cursor() as cursor:  # Add user
            cursor.execute(sql, (username, pwhash))
            conn.commit()
    username = ""
    print("User created Successfully\n")


def login():
    user = username_input("Username: ")
    password = getpass.getpass("Password: ")
    if user == "":
        return
    elif check(user, password.encode('utf-8')):
        print("Logged in\n")
    else:
        print("Incorrect Username or Password")
        print("Please try again\n")


def __main__():
    while True:
        print('0: Login\n1: Create a new Login\n2: Change your username\n3: Change your password')
        num = int(sys.stdin.readline()[0])
        if num == 0:
            login()
        elif num == 1:
            create()
        elif num == 2:
            print("in progress")
        elif num == 3:
            print("in progress")


__main__()
