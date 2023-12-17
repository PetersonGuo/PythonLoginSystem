import twofactor
import user
import sql
import bcrypt
import getpass


def create_account():
    username = create_username()
    uid = sql.insert(username, create_password(username))
    print("\nWould you like to setup 2FA? (y/n)")
    if user.yes_no_input():
        twofactor.setup_2fa(uid)
    print("User created Successfully\n")


def create_username():
    username = ""
    while username == "":
        username = user.username_input("Enter a new username: ")
        if len(username) == 0:
            continue
        elif sql.get_user_id(username) is not None:
            print("That username is already taken")
            username = ""
    return username


def create_password(username):
    print(
        "\nDo not use common passwords\nUse Letters, Numbers, and Symbols\nDo not use common "
        "english words in your password\nDo not use your name, username, birthday, or other personal "
        "information\nMust be at least 12 characters long")

    pw = ""
    while pw == "":
        pw = getpass.getpass('\nEnter a new password: ')
        if user.is_valid_password(username, pw):
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
