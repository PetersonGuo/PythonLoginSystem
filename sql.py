import os
import pymysql.cursors


def connect():
    return pymysql.connect(host=os.getenv('database_host'),
                           user=os.getenv('database_user'),
                           password=os.getenv('database_pass'),
                           database=os.getenv('database_name'),
                           cursorclass=pymysql.cursors.DictCursor)


def getuser(username):
    conn = connect()
    with conn:
        sql = "SELECT * FROM `User` WHERE `Username`=%s"
        conn.ping()
        with conn.cursor() as cursor:
            cursor.execute(sql, username)
            result = cursor.fetchone()
    return result


def insert(username, pwhash):
    conn = connect()
    with conn:
        sql = "INSERT INTO `User` (Username, Password) VALUES (%s, %s)"
        conn.ping()
        with conn.cursor() as cursor:  # Add user
            cursor.execute(sql, (username, pwhash))
            conn.commit()
