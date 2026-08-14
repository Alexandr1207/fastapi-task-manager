import jwt
from datetime import datetime, timedelta, timezone
from pwdlib import PasswordHash
import os


from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


pass_hash = PasswordHash.recommended()


def hash_password(password: str) -> str:
    hashed_password = pass_hash.hash(password)
    return hashed_password


def verify_password(password: str, hashed_password: str) -> bool:
    return pass_hash.verify(
        password=password,
        hash=hashed_password
    )


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


token = create_access_token({
    "sub": "1",
    "role": "user"
})

print(token)