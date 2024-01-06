import os
import pymysql.cursors


def connect():
    try:
        return pymysql.connect(host=os.getenv('database_host'),
                               user=os.getenv('database_user'),
                               password=os.getenv('database_pass'),
                               database=os.getenv('database_name'),
                               cursorclass=pymysql.cursors.DictCursor,
                               connect_timeout=1)
    except pymysql.err.OperationalError:
        print("Could not connect to database")
        exit(1)


def get_sql(sql, *args):
    conn = connect()
    try:
        with conn.cursor() as cursor:
            cursor.execute(sql, *args)
            result = cursor.fetchone()
    except pymysql.err.OperationalError:
        print("Could not connect to database")
        exit(1)
    finally:
        conn.close()
    return result


def update_sql(sql, *args):
    conn = connect()
    try:
        with conn.cursor() as cursor:
            cursor.execute(sql, *args)
            conn.commit()
    except pymysql.err.OperationalError:
        print("Could not connect to database")
        exit(1)
    finally:
        conn.close()


def get_username(user):
    result = get_sql("SELECT Username FROM `User` WHERE `UID`=%s", user.uid)
    try:
        return result['Username']
    except TypeError:
        return None


def get_encoded_pw(user):
    result = get_sql("SELECT Password FROM `User` WHERE `UID`=%s", user.uid)
    try:
        return result['Password']
    except TypeError:
        return None


def get_2fa_secret(user):
    result = get_sql("SELECT 2FA_Secret FROM `User` WHERE `UID`=%s", user.uid)
    try:
        return result['2FA_Secret']
    except TypeError:
        return None


def get_user_id(username: str):
    result = get_sql("SELECT UID FROM `User` WHERE `Username`=%s", username)
    try:
        return result['UID']
    except TypeError:
        return None


def insert(username: str, pwhash):
    update_sql("INSERT INTO `User` (Username, Password) VALUES (%s, %s)", (username, pwhash))
    return get_user_id(username)


def insert_email(username: str, email: str, pwhash):
    update_sql("INSERT INTO `User` (Username, Email, Password) VALUES (%s, %s, %s)", (username, email, pwhash))
    return get_user_id(username)


def insert_2fa(user, secret):
    update_sql("UPDATE `User` SET `2FA_Secret`=%s WHERE `UID`=%s", (secret, user.uid))


def change_username(user, new_username: str):
    update_sql("UPDATE `User` SET `Username`=%s WHERE `UID`=%s", (new_username, user.uid))


def change_password(user, new_password):
    update_sql("UPDATE `User` SET `Password`=%s WHERE `UID`=%s", (new_password, user.uid))


def delete_user(user):
    update_sql("DELETE FROM `User` WHERE `UID`=%s", user.uid)


def remove_2fa(user):
    update_sql("UPDATE `User` SET `2FA_Secret`=NULL WHERE `UID`=%s", user.uid)


def get_email(user):
    result = get_sql("SELECT Email FROM `User` WHERE `UID`=%s", user.uid)
    try:
        return result['Email']
    except TypeError:
        return None
