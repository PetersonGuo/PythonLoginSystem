import sys


def yes_no_input():
    yn = ""
    try:
        yn = sys.stdin.readline()[0].lower()
    except ValueError:
        print("Invalid Input")
    return yn == "y"
