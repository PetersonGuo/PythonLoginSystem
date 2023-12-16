# To Implement:
# User Timeout/Brute force prevention
# User account control
# Password strength
# Error catching with SQL
# frontend and flask

import sys
import dotenv
import login
import create
import twofactor

dotenv.load_dotenv()


def __main__():
    user = None
    while True:
        print('0: Login\n1: Create a new Login\n2: Change your username\n3: Change your password\n4: Setup 2FA'
              '\n5: Logout')
        try:
            num = int(sys.stdin.readline()[0])
        except ValueError:
            print("Invalid Input")
            continue

        match num:
            case 0:
                user = login.login()
            case 1:
                create.create()
            case 2:
                if user is not None:
                    print("in progress")
                else:
                    print("Please sign in first")
            case 3:
                if user is not None:
                    print("in progress")
                else:
                    print("Please sign in first")
            case 4:
                twofactor.two_factor_authenticate(user)
            case 5:
                user = None
                print("Logged out\n")
            case _:
                print("Invalid Input")


__main__()
