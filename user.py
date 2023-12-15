import sys
import re


def username_input(str1):
    print(str1)
    username = sys.stdin.readline().strip()
    if is_valid_username(username):
        return username
    return ""


def is_valid_username(str1):
    if len(str1) < 4:
        print("Username must be at least 4 characters long")
        return False
    elif len(str1) > 20:
        print("Username must be less than 20 characters long")
        return False
    elif re.search(r'[^A-Za-z0-9_.-]', str1):
        print("Invalid characters in username")
        return False
    else:
        return True
