import getpass
import sys
import create
import login
import sql
import twofactor


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


def setup_2fa(uid):
    secret = twofactor.generate_qr_code(uid)
    if secret is not None:
        sql.insert_2fa(uid, secret)


def remove_2fa(uid):
    print("Are you sure you want to remove 2FA? (y/n)")
    if yes_no_input():
        if __reauthenticate(uid):
            sql.remove_2fa(uid)
            print("2FA removed")
            return True
    print("2FA not removed")
    return False


def is_2fa_setup(uid):
    return sql.get_2fa_secret(uid) is not None
