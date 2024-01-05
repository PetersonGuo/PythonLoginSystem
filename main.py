# To Implement:
# User Timeout/Brute force prevention
# Password strength
# Password reset
# Email verification
# frontend

import sys
import dotenv
import login
import create
import os

try:
    os.system('clear')
except:
    os.system('cls')

dotenv.load_dotenv()


def __main__():
    session_user = None
    while True:
        if session_user is None:
            print('0: Login\n1: Create a new Login')
        elif session_user.is_2fa_setup():
            print('0: Change your username\n1: Change your password\n2: Remove 2FA\n3: Logout\n4: Delete Account')
        else:
            print('0: Change your username\n1: Change your password\n2: Setup 2FA\n3: Logout\n4: Delete Account')

        try:
            num = int(sys.stdin.readline()[0])
        except ValueError:
            print("Invalid Input")
            continue

        if session_user is None:
            match num:
                case 0:
                    session_user = login.login()
                case 1:
                    create.create_account()
                case _:
                    print("Invalid Input")
        else:
            match num:
                case 0:
                    session_user.change_username()
                case 1:
                    session_user.change_password()
                case 2:
                    if session_user.is_2fa_setup():
                        session_user.remove_2fa()
                    else:
                        session_user.setup_2fa()
                case 3:
                    print("Logged out\n")
                    session_user = None
                case 4:
                    if session_user.delete_account():
                        session_user = None
                case _:
                    print("Invalid Input")


__main__()
