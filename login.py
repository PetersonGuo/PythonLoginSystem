import sys
import re
import hashlib
import pymssql

logins = {
    "pete":hashlib.sha512("1234".encode('utf-16')).hexdigest()
}

conn = pymssql.connect("localhost", "sa", "", "LOGINS")
cursor = conn.cursor(as_dict=True)

def check(username, pw):
    print(pw)
    if username in logins:
        if logins[username] == pw:
            return True
    return False

def regex(string):
    if not(re.search(r"[\w@\$\d\s.,]", string)):
        return True
    return False

def create():
    username = ""
    while username == "":
        print("Enter a new username: ")
        username = sys.stdin.readline()
        username = username[0 : len(username) - 1]
        if regex(username):
            print("Invalid characters in username")
            username = ""
        elif username in logins:
            print("That username is already taken")
            username = ""

    print("\nSome password tips\nDo not use common passwords\nUse Letters, Numbers, and Symbols\nDo not use common english words in your password\nDo not use your name, birthday, or other personal information")
    pw = ""
    while pw == "":
        print("\nEnter a new password: ")
        pw = sys.stdin.readline()
        if len(pw) < 13:
            print("Password must be at least 12 characters long")
            pw = ""
        elif username in pw:
            print("Password cannot contain your username")
            pw = ""
    cursor.execute("INSERT INTO USERS ('Name', 'Password') VALUES ("+username+", "+hashlib.sha512(pw[0 : len(pw) - 1].encode('utf-16')).hexdigest()+");")
    cursor.commit()
    logins[username] = hashlib.sha512(pw[0 : len(pw) - 1].encode('utf-16')).hexdigest()

tries = 3
while tries != 0:
    print("Type 'create' to make a new username and password")
    print("Username: ")
    user = sys.stdin.readline()
    user = user[0 : len(user) - 1]
    if (user.lower() == "create"):
        create()
    else:
        print("Password: ")
        password = sys.stdin.readline()
        password = password[0 : len(password) - 1]
        if password.lower() == "create":
            create()
        else: 
            if check(user, hashlib.sha512(password.encode('utf-16')).hexdigest()):
                print("Logged in")
                break
            else:
                print("Incorrect Username or Password")
                print("Please try again")
                tries -= 1
