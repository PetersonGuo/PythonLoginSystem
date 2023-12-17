# To Implement:
# User Timeout/Brute force prevention
# Password strength
# frontend and flask

import sys
import dotenv
import login
import create
import user

dotenv.load_dotenv()


def __main__():
    uid = None
    while True:
        if uid is None:
            print('0: Login\n1: Create a new Login')
        elif user.is_2fa_setup(uid):
            print('0: Change your username\n1: Change your password\n2: Remove 2FA\n3: Logout\n4: Delete Account')
        else:
            print('0: Change your username\n1: Change your password\n2: Setup 2FA\n3: Logout\n4: Delete Account')

        try:
            num = int(sys.stdin.readline()[0])
        except ValueError:
            print("Invalid Input")
            continue

        if uid is None:
            match num:
                case 0:
                    uid = login.login()
                case 1:
                    create.create_account()
                case _:
                    print("Invalid Input")
        else:
            match num:
                case 0:
                    user.change_username(uid)
                case 1:
                    user.change_password(uid)
                case 2:
                    if user.is_2fa_setup(uid):
                        user.remove_2fa(uid)
                    else:
                        user.setup_2fa(uid)
                case 3:
                    print("Logged out\n")
                    uid = None
                case 4:
                    if user.delete_user(uid):
                        uid = None
                case _:
                    print("Invalid Input")


__main__()
