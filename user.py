import getpass
import sys
import create
import login
import sql
import twofactor


class User:
    def __init__(self, uid):
        self.uid = None
        self.username = None
        self.hash = None
        self.init(uid, sql.get_username(uid), sql.get_encoded_pw(uid))

    def init(self, uid, username, encoded_pw):
        self.uid = uid
        self.username = username
        self.hash = encoded_pw

    def __reauthenticate__(self):  # Use password and 2fa to reauthenticate
        password = getpass.getpass("Password: ")
        if login.check(sql.get_username(self.uid), password.encode('utf-8')):
            if sql.get_2fa_secret(self.uid) is not None:
                if login.twofactor_loop(self.uid):
                    return True
            else:
                return True
        else:
            print("Incorrect Password")
        return False

    def change_username(self):  # Use password and 2fa to change username
        print("Are you sure you want to change your username? (y/n)")
        if yes_no_input():
            if self.__reauthenticate__():
                sql.change_username(self.uid, create.create_username())
                print('Username changed')
                return True
        print('Username not changed')
        return False

    def change_password(self):  # Use password and 2fa to change password
        print("Are you sure you want to change your password? (y/n)")
        if yes_no_input():
            if self.__reauthenticate__():
                sql.change_password(self.uid, create.create_password(self.username))
                print('Password changed')
                return True
        print('Password not changed')
        return False

    def delete_account(self):   # Use password and 2fa to delete account
        print("Are you sure you want to delete your account? (y/n)")
        if yes_no_input():
            if self.__reauthenticate__():
                sql.delete_user(self.uid)
                print('Account deleted')
                return True
        print('Account not deleted')
        return False

    def setup_2fa(self):
        secret = twofactor.generate_qr_code(self.uid)
        if secret is not None:
            sql.insert_2fa(self.uid, secret)

    def remove_2fa(self):
        print("Are you sure you want to remove 2FA? (y/n)")
        if yes_no_input():
            if self.__reauthenticate__():
                sql.remove_2fa(self.uid)
                print("2FA removed")
                return True
        print("2FA not removed")
        return False

    def is_2fa_setup(self):
        return sql.get_2fa_secret(self.uid) is not None


def yes_no_input():
    yn = ""
    try:
        yn = sys.stdin.readline()[0].lower()
    except ValueError:
        print("Invalid Input")
    return yn == "y"
