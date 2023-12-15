# To Implement:
# User Timeout/Brute force prevention
# User account control
# 2FA
# Password strength
# Error catching with SQL
# frontend and flask

import sys
import dotenv
import login
import create

dotenv.load_dotenv()


def __main__():
    loggedin = False
    while True:
        print('0: Login\n1: Create a new Login\n2: Change your username\n3: Change your password\n4: Logout')
        num = int(sys.stdin.readline()[0])
        if num == 0:
            loggedin = login.login()
        elif num == 1:
            create.create()
        elif num == 2:
            if loggedin:
                print("in progress")
            else:
                print("Please sign in first")
        elif num == 3:
            if loggedin:
                print("in progress")
            else:
                print("Please sign in first")
        elif num == 4:
            loggedin = False
            print("Logged out\n")


__main__()
