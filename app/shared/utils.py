from passlib.context import CryptContext

pwd_context = CryptContext(
    schemes=["argon2", "bcrypt"],
    deprecated="auto",
)

def hash_password(*, password: str) -> str:
    if not isinstance(password, str) or not password:
        raise ValueError("Password must be a non-empty string")
    return pwd_context.hash(password)

def verify_password(*, plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def normalize_email(email: str) -> str:
    return email.strip().lower()