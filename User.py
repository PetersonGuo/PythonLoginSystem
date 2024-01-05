import create
import login
import sql
import twofactor
import user
from getpass import getpass


class User:
    def __init__(self, uid, username, email=None):
        if username is None:
            raise ValueError("Username cannot be None")
        self.uid = uid
        self.username = username
        self.email = email

    def __reauthenticate__(self):  # Use password and 2fa to reauthenticate
        if login.check(self, getpass("Password: ").encode('utf-8')):
            if sql.get_2fa_secret(self) is not None:
                if login.twofactor_loop(self):
                    return True
            else:
                return True
        else:
            print("Incorrect Password")
        return False

    def change_username(self):  # Use password and 2fa to change username
        print("Are you sure you want to change your username? (y/n)")
        if user.yes_no_input():
            if self.__reauthenticate__():
                sql.change_username(self, create.create_username())
                print('Username changed')
                return True
        print('Username not changed')
        return False

    def change_password(self):  # Use password and 2fa to change password
        print("Are you sure you want to change your password? (y/n)")
        if user.yes_no_input():
            if self.__reauthenticate__():
                sql.change_password(self, create.create_password(self.username))
                print('Password changed')
                return True
        print('Password not changed')
        return False

    def delete_account(self):   # Use password and 2fa to delete account
        print("Are you sure you want to delete your account? (y/n)")
        if user.yes_no_input():
            if self.__reauthenticate__():
                sql.delete_user(self)
                print('Account deleted')
                return True
        print('Account not deleted')
        return False

    def setup_2fa(self):
        secret = twofactor.generate_qr_code(self)
        if secret is not None:
            sql.insert_2fa(self, secret)

    def remove_2fa(self):
        print("Are you sure you want to remove 2FA? (y/n)")
        if user.yes_no_input():
            if self.__reauthenticate__():
                sql.remove_2fa(self)
                print("2FA removed")
                return True
        print("2FA not removed")
        return False

    def is_2fa_setup(self):
        return sql.get_2fa_secret(self) is not None

