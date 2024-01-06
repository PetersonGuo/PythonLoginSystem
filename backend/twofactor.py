import pyotp
import pyqrcode


def generate_qr_code(user):
    secret = pyotp.random_base32()
    auth = pyotp.totp.TOTP(secret).provisioning_uri(
        name=user.username,
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
