from passlib.hash import bcrypt

def hashing(password):
    return bcrypt.hash(password)

def verify_password(plain_password, harshed_password):
    return bcrypt.verify(plain_password, harshed_password) # This compared the passwords