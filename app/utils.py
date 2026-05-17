from pwdlib import PasswordHash

password_hash = PasswordHash.recommended()

def hash(password: str):
    """Converts plain text password into a secure hash for storage."""
    return password_hash.hash(password)

def verify(plain_password: str, hashed_password: str):
    """Compares the login password against the stored hash."""
    return password_hash.verify(plain_password, hashed_password)