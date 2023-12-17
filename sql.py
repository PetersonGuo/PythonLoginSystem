import os
import pymysql.cursors


def connect():
    return pymysql.connect(host=os.getenv('database_host'),
                           user=os.getenv('database_user'),
                           password=os.getenv('database_pass'),
                           database=os.getenv('database_name'),
                           cursorclass=pymysql.cursors.DictCursor)


def get_sql(sql, *args):
    conn = connect()
    with conn:
        conn.ping()
        with conn.cursor() as cursor:
            cursor.execute(sql, *args)
            result = cursor.fetchone()
    return result


def update_sql(sql, *args):
    conn = connect()
    with conn:
        conn.ping()
        with conn.cursor() as cursor:
            cursor.execute(sql, *args)
            conn.commit()


def get_username(uid):
    result = get_sql("SELECT Username FROM `User` WHERE `UID`=%s", uid)
    try:
        return result['Username']
    except TypeError:
        return None


def get_encoded_pw(uid):
    result = get_sql("SELECT Password FROM `User` WHERE `UID`=%s", uid)
    try:
        return result['Password']
    except TypeError:
        return None


def get_2fa_secret(uid):
    result = get_sql("SELECT 2FA_Secret FROM `User` WHERE `UID`=%s", uid)
    try:
        return result['2FA_Secret']
    except TypeError:
        return None


def get_user_id(username):
    result = get_sql("SELECT UID FROM `User` WHERE `Username`=%s", username)
    try:
        return result['UID']
    except TypeError:
        return None


def insert(username, pwhash):
    update_sql("INSERT INTO `User` (Username, Password) VALUES (%s, %s)", (username, pwhash))
    return get_user_id(username)


def insert_2fa(uid, secret):
    update_sql("UPDATE `User` SET `2FA_Secret`=%s WHERE `UID`=%s", (secret, uid))


def change_username(uid, new_username):
    update_sql("UPDATE `User` SET `Username`=%s WHERE `UID`=%s", (new_username, uid))


def change_password(uid, new_password):
    update_sql("UPDATE `User` SET `Password`=%s WHERE `UID`=%s", (new_password, uid))


def delete_user(uid):
    update_sql("DELETE FROM `User` WHERE `UID`=%s", uid)


def remove_2fa(uid):
    update_sql("UPDATE `User` SET `2FA_Secret`=NULL WHERE `UID`=%s", uid)
