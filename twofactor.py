import pyotp
import pyqrcode
import sql
import user


def setup_2fa(uid):
    secret = generate_qr_code(uid)
    if secret is not None:
        sql.insert_2fa(uid, secret)


def generate_qr_code(uid):
    username = sql.get_username(uid)
    secret = pyotp.random_base32()
    auth = pyotp.totp.TOTP(secret).provisioning_uri(
        name=username,
        issuer_name='Login_System')
    print(pyqrcode.create(auth).terminal(quiet_zone=1))
    print("Scan the QR code with your phone")
    print("Or enter this code manually: " + secret)
    if verify_code(secret):
        print("2FA setup successfully")
        return secret
    else:
        print("2FA setup failed")
        return None


def verify_code(secret):
    totp = pyotp.TOTP(secret)
    return totp.verify(input("Enter the Code: ").strip().replace(" ", ""))


def remove_2fa(uid):
    print("Are you sure you want to remove 2FA? (y/n)")
    if user.yes_no_input():
        if user.__reauthenticate(uid):
            sql.remove_2fa(uid)
            print("2FA removed")
            return True
    print("2FA not removed")
    return False


def is_2fa_setup(uid):
    return sql.get_2fa_secret(uid) is not None
