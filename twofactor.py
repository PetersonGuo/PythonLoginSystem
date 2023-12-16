import pyotp
import pyqrcode
import sql


def two_factor_authenticate(user):
    if user is not None:
        if sql.get_2fa_secret(user)['2FA_Secret'] is not None:
            print("2FA already setup")
            return
        secret = generate_qr_code(user)
        if secret is not None:
            sql.insert_2fa(user, secret)
    else:
        print("Please sign in first")


def generate_qr_code(username):
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
    return totp.verify(input("Enter the Code : "))
