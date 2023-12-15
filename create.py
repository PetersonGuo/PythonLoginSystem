import user
import sql
import bcrypt
import getpass


def create():
    username = ""
    while username == "":
        username = user.username_input("Enter a new username: ")
        if len(username) == 0:
            continue
        elif sql.getuser(username) is not None:
            print("That username is already taken")
            username = ""

    print(
        "\nDo not use common passwords\nUse Letters, Numbers, and Symbols\nDo not use common "
        "english words in your password\nDo not use your name, username, birthday, or other personal "
        "information\nMust be at least 12 characters long")

    pw = ""
    while pw == "":
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
    sql.insert(username, pwhash)
    username = ""
    print("User created Successfully\n")
