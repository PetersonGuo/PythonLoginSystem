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
        sql = "SELECT Username FROM `User` WHERE `Username`=%s"
        conn.ping()
        with conn.cursor() as cursor:
            cursor.execute(sql, username)
            result = cursor.fetchone()
    return result


def get_encoded_pw(username):
    conn = connect()
    with conn:
        sql = "SELECT Password FROM `User` WHERE `Username`=%s"
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


def insert_2fa(username, secret):
    conn = connect()
    with conn:
        sql = "UPDATE `User` SET `2FA_Secret`=%s WHERE `Username`=%s"
        conn.ping()
        with conn.cursor() as cursor:
            cursor.execute(sql, (secret, username))
            conn.commit()


def get_2fa_secret(username):
    conn = connect()
    with conn:
        sql = "SELECT 2FA_Secret FROM `User` WHERE `Username`=%s"
        conn.ping()
        with conn.cursor() as cursor:
            cursor.execute(sql, username)
            result = cursor.fetchone()
    return result
